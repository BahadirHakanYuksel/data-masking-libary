"""
Command line interface for the data masking library.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict

import click
import yaml

from .masker import DataMasker
from .config import MaskingConfig, MaskingStrategy


@click.group()
@click.version_option()
def main():
    """Data Masking Library CLI - Mask PII in your data."""
    pass


@main.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file')
@click.option('--strategy', '-s', type=click.Choice(['replace', 'redact', 'encrypt', 'tokenize', 'faker']), 
              default='replace', help='Masking strategy')
@click.option('--preserve-format/--no-preserve-format', default=True, 
              help='Preserve original format')
@click.option('--partial-mask/--full-mask', default=True, 
              help='Partially mask values')
@click.option('--confidence-threshold', '-t', type=float, default=0.8, 
              help='Confidence threshold for PII detection')
def mask(input_file, output_file, config, strategy, preserve_format, partial_mask, confidence_threshold):
    """Mask PII in a file."""
    
    # Load configuration
    if config:
        config_data = load_config(config)
        masking_config = MaskingConfig(**config_data)
    else:
        masking_config = MaskingConfig(
            strategy=MaskingStrategy(strategy),
            preserve_format=preserve_format,
            partial_mask=partial_mask,
            confidence_threshold=confidence_threshold
        )
    
    # Load input data
    input_path = Path(input_file)
    try:
        if input_path.suffix.lower() == '.json':
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        elif input_path.suffix.lower() in ['.yml', '.yaml']:
            with open(input_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        else:
            # Treat as text file
            with open(input_path, 'r', encoding='utf-8') as f:
                data = f.read()
    except Exception as e:
        click.echo(f"Error loading input file: {e}", err=True)
        sys.exit(1)
    
    # Mask the data
    masker = DataMasker(masking_config)
    masked_data = masker.mask(data)
    
    # Save output
    output_path = Path(output_file)
    try:
        if output_path.suffix.lower() == '.json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(masked_data, f, indent=2, ensure_ascii=False)
        elif output_path.suffix.lower() in ['.yml', '.yaml']:
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(masked_data, f, default_flow_style=False)
        else:
            # Treat as text file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(str(masked_data))
    except Exception as e:
        click.echo(f"Error saving output file: {e}", err=True)
        sys.exit(1)
    
    click.echo(f"Successfully masked data and saved to {output_file}")


@main.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file')
@click.option('--confidence-threshold', '-t', type=float, default=0.8, 
              help='Confidence threshold for PII detection')
@click.option('--format', '-f', type=click.Choice(['json', 'yaml', 'table']), 
              default='table', help='Output format')
def analyze(input_file, config, confidence_threshold, format):
    """Analyze PII in a file without masking."""
    
    # Load configuration
    if config:
        config_data = load_config(config)
        masking_config = MaskingConfig(**config_data)
    else:
        masking_config = MaskingConfig(confidence_threshold=confidence_threshold)
    
    # Load input data
    input_path = Path(input_file)
    try:
        if input_path.suffix.lower() == '.json':
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        elif input_path.suffix.lower() in ['.yml', '.yaml']:
            with open(input_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        else:
            # Treat as text file
            with open(input_path, 'r', encoding='utf-8') as f:
                data = f.read()
    except Exception as e:
        click.echo(f"Error loading input file: {e}", err=True)
        sys.exit(1)
    
    # Analyze the data
    masker = DataMasker(masking_config)
    analysis = masker.analyze(data)
    
    # Output results
    if format == 'json':
        # Convert PIIMatch objects to dictionaries for JSON serialization
        if 'matches' in analysis:
            analysis['matches'] = [
                {
                    'text': match.text,
                    'start': match.start,
                    'end': match.end,
                    'pattern_name': match.pattern_name,
                    'confidence': match.confidence,
                    'category': match.category
                }
                for match in analysis['matches']
            ]
        click.echo(json.dumps(analysis, indent=2))
    elif format == 'yaml':
        if 'matches' in analysis:
            analysis['matches'] = [
                {
                    'text': match.text,
                    'start': match.start,
                    'end': match.end,
                    'pattern_name': match.pattern_name,
                    'confidence': match.confidence,
                    'category': match.category
                }
                for match in analysis['matches']
            ]
        click.echo(yaml.dump(analysis, default_flow_style=False))
    else:
        # Table format
        click.echo("PII Analysis Results")
        click.echo("===================")
        click.echo(f"Total matches: {analysis['total_matches']}")
        
        if analysis['categories']:
            click.echo("\nBy Category:")
            for category, count in analysis['categories'].items():
                click.echo(f"  {category}: {count}")
        
        if analysis['patterns']:
            click.echo("\nBy Pattern:")
            for pattern, count in analysis['patterns'].items():
                click.echo(f"  {pattern}: {count}")
        
        conf_dist = analysis['confidence_distribution']
        click.echo(f"\nConfidence Distribution:")
        click.echo(f"  High (≥0.9): {conf_dist['high']}")
        click.echo(f"  Medium (≥0.7): {conf_dist['medium']}")
        click.echo(f"  Low (<0.7): {conf_dist['low']}")


@main.command()
@click.argument('output_file', type=click.Path())
def generate_config(output_file):
    """Generate a sample configuration file."""
    config = MaskingConfig()
    config_dict = config.dict()
    
    output_path = Path(output_file)
    try:
        if output_path.suffix.lower() in ['.yml', '.yaml']:
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(config_dict, f, default_flow_style=False)
        else:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2)
    except Exception as e:
        click.echo(f"Error saving config file: {e}", err=True)
        sys.exit(1)
    
    click.echo(f"Sample configuration saved to {output_file}")


def load_config(config_file: str) -> Dict[str, Any]:
    """Load configuration from file."""
    config_path = Path(config_file)
    
    try:
        if config_path.suffix.lower() in ['.yml', '.yaml']:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        else:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        click.echo(f"Error loading config file: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
