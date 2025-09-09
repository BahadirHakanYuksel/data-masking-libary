#!/bin/bash

echo "🛡️ DATA MASKING LIBRARY - FINAL DEMONSTRATION"
echo "============================================="

cd /home/bhy/Desktop/bhy-pro/projects/data-masking-library

echo "📊 Running comprehensive test suite..."
PYTHONPATH=src python3 -m pytest tests/ -q
echo ""

echo "🔍 Analyzing sample data for PII..."
PYTHONPATH=src python3 -m data_masker.cli analyze examples/sample_data.json --format table
echo ""

echo "🛡️ Masking sample data..."
PYTHONPATH=src python3 -m data_masker.cli mask examples/sample_data.json examples/final_masked.json
echo ""

echo "📝 Generating configuration file..."
PYTHONPATH=src python3 -m data_masker.cli generate-config examples/sample_config.json
echo ""

echo "✅ DEMONSTRATION COMPLETE!"
echo "=========================="
echo ""
echo "🎉 Data Masking Library is fully functional and ready for:"
echo "   • Enterprise deployment"
echo "   • Open source distribution"
echo "   • Community contributions"
echo ""
echo "📁 Key files created:"
echo "   • examples/final_masked.json - Masked data output"
echo "   • examples/sample_config.json - Configuration template"
echo ""
echo "🚀 Next steps:"
echo "   • Publish to PyPI"
echo "   • Create GitHub repository"
echo "   • Continue with other open source projects"
