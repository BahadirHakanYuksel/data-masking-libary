"""
Test the CLI functionality.
"""

import json
import tempfile
from pathlib import Path
from click.testing import CliRunner

from data_masker.cli import main


class TestCLI:
    """Test cases for CLI functionality."""
    
    def test_mask_json_file(self):
        """Test masking a JSON file."""
        runner = CliRunner()
        
        # Create test data
        test_data = {
            "users": [
                {
                    "name": "John Doe",
                    "email": "john@example.com",
                    "phone": "555-123-4567"
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            input_file = f.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            output_file = f.name
        
        try:
            result = runner.invoke(main, ['mask', input_file, output_file])
            
            assert result.exit_code == 0
            assert "Successfully masked" in result.output
            
            # Check output file
            with open(output_file, 'r') as f:
                masked_data = json.load(f)
            
            # Email should be masked but domain preserved
            masked_email = masked_data["users"][0]["email"]
            assert "john@example.com" != masked_email
            assert "@example.com" in masked_email
            
        finally:
            Path(input_file).unlink()
            Path(output_file).unlink()
    
    def test_analyze_text_file(self):
        """Test analyzing a text file."""
        runner = CliRunner()
        
        test_text = "Contact John Doe at john@example.com or 555-123-4567"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(test_text)
            input_file = f.name
        
        try:
            result = runner.invoke(main, ['analyze', input_file])
            
            assert result.exit_code == 0
            assert "PII Analysis Results" in result.output
            assert "Total matches:" in result.output
            
        finally:
            Path(input_file).unlink()
    
    def test_generate_config(self):
        """Test generating a configuration file."""
        runner = CliRunner()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            config_file = f.name
        
        try:
            result = runner.invoke(main, ['generate-config', config_file])
            
            assert result.exit_code == 0
            assert "Sample configuration saved" in result.output
            
            # Check config file was created
            with open(config_file, 'r') as f:
                config_data = json.load(f)
            
            assert "strategy" in config_data
            assert "preserve_format" in config_data
            
        finally:
            Path(config_file).unlink()
    
    def test_mask_with_custom_strategy(self):
        """Test masking with custom strategy."""
        runner = CliRunner()
        
        test_data = {"email": "test@example.com"}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            input_file = f.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            output_file = f.name
        
        try:
            result = runner.invoke(main, [
                'mask', input_file, output_file,
                '--strategy', 'redact'
            ])
            
            assert result.exit_code == 0
            
            # Check redaction was applied
            with open(output_file, 'r') as f:
                masked_data = json.load(f)
            
            assert "[REDACTED]" in masked_data["email"]
            
        finally:
            Path(input_file).unlink()
            Path(output_file).unlink()
