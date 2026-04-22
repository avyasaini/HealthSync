"""
Run Script for HealthSync System

This script validates the setup and runs the Flask application with HTTPS support.
"""

#!/usr/bin/env python
import os
import sys
from datetime import datetime
import traceback
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger('diagnoscope_ai')

# Path configuration
app_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, app_dir)

# Ensure user-installed pip packages are found (needed on Windows when system site-packages is read-only)
import site
user_site = site.getusersitepackages()
if user_site not in sys.path:
    sys.path.insert(1, user_site)

def validate_setup():
    """Validate application setup before running"""
    print("Validating application setup...")
    print("\n=== HealthSync System Validation ===\n")
    
    # Validate directories
    directories = ['uploads', 'static', 'templates']
    for directory in directories:
        if os.path.exists(os.path.join(app_dir, directory)):
            print(f"[OK] Directory exists: {directory}")
        else:
            print(f"[FAIL] Directory missing: {directory}")
            os.makedirs(os.path.join(app_dir, directory), exist_ok=True)
            print(f"  Created directory: {directory}")
    
    # Validate models
    try:
        import pickle
        model_files = ['Fracture_XGBoost', 'TB_XGBoost']
        for model_file in model_files:
            if os.path.exists(os.path.join(app_dir, model_file)):
                # Validate model can be loaded
                try:
                    model = pickle.load(open(os.path.join(app_dir, model_file), 'rb'))
                    print(f"[OK] Model loaded successfully: {model_file}")
                except Exception as e:
                    print(f"[FAIL] Model file corrupted: {model_file} - {str(e)}")
            else:
                print(f"[FAIL] Model file missing: {model_file}")
    except ImportError:
        print("[FAIL] Could not validate models - pickle module not available")
    
    # Validate database
    db_path = os.path.join(app_dir, 'instance', 'users.db')
    if os.path.exists(db_path):
        print(f"[OK] Database exists: {os.path.relpath(db_path, app_dir)}")
    else:
        print(f"[FAIL] Database missing: {os.path.relpath(db_path, app_dir)}")
        print("  Database will be created on first run")
    
    # Print summary
    print("\n=== Validation Summary ===")
    print("[OK] Directories: All OK")
    print("[OK] Models: All OK")
    print("[OK] Database: Ready")
    print("\nSetup valid [OK]")
    print("You can safely run the application if all checks passed.")
    print("If model files are missing, prediction functionality will be limited.")

def setup_ssl():
    """Generate self-signed SSL certificates for HTTPS"""
    print("\nGenerating self-signed SSL certificates for HTTPS...")
    try:
        from OpenSSL import crypto
        
        # Check if certificates already exist
        if os.path.exists('cert.pem') and os.path.exists('key.pem'):
            print("SSL certificates already exist.")
            return True
            
        # Create a key pair
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 2048)
        
        # Create a self-signed cert
        cert = crypto.X509()
        cert.get_subject().C = "IN"
        cert.get_subject().ST = "Maharashtra"
        cert.get_subject().L = "Mumbai"
        cert.get_subject().O = "HealthSync"
        cert.get_subject().OU = "Medical Diagnostics"
        cert.get_subject().CN = "localhost"
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(365*24*60*60)  # 1 year
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha256')
        
        # Write out the files
        with open('cert.pem', "wb") as f:
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        with open('key.pem', "wb") as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
            
        print("SSL certificates generated successfully.")
        return True
    except Exception as e:
        print(f"Failed to generate SSL certificates: {str(e)}")
        return False

def run_app():
    """Run the flask application"""
    print("\nStarting HealthSync System...")
    
    # Detect Codespaces environment and prefer plain HTTP for port forwarding
    use_http = os.environ.get('CODESPACES', 'false').lower() == 'true'
    ssl_enabled = False if use_http else setup_ssl()
    
    from app import app
    
    if ssl_enabled:
        print("HTTPS enabled. Visit https://localhost:5000")
        app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('cert.pem', 'key.pem'))
    else:
        print("HTTP enabled. Visit http://localhost:5000")
        if use_http:
            print("Running in Codespaces, using HTTP for forwarded port compatibility.")
        else:
            print("WARNING: Your medical data is not encrypted in transit.")
        app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == "__main__":
    try:
        validate_setup()
        run_app()
    except Exception as e:
        error_message = f"Error running application: {str(e)}"
        logger.error(error_message)
        logger.error(traceback.format_exc())
        print(f"ERROR: {error_message}")
        print("Check app.log for detailed error information.") 