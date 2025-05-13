#!/usr/bin/env python
"""
Azure deployment utility script for TahubuSF FastAPI server
"""
import argparse
import json
import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("tahubu_sf.azure_deploy")

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

def run_command(cmd, check=True):
    """Run a shell command and log output"""
    logger.info(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=check, capture_output=True, text=True)
    if result.stdout:
        logger.info(result.stdout)
    if result.stderr:
        if result.returncode != 0:
            logger.error(result.stderr)
        else:
            logger.warning(result.stderr)
    return result

def create_resource_group(args):
    """Create Azure resource group"""
    logger.info(f"Creating resource group: {args.resource_group}")
    run_command([
        "az", "group", "create",
        "--name", args.resource_group,
        "--location", args.location
    ])

def create_app_service_plan(args):
    """Create Azure App Service Plan"""
    logger.info(f"Creating App Service Plan: {args.plan_name}")
    run_command([
        "az", "appservice", "plan", "create",
        "--name", args.plan_name,
        "--resource-group", args.resource_group,
        "--sku", args.sku,
        "--is-linux"
    ])

def create_web_app(args):
    """Create Azure Web App"""
    logger.info(f"Creating Web App: {args.app_name}")
    run_command([
        "az", "webapp", "create",
        "--name", args.app_name,
        "--resource-group", args.resource_group,
        "--plan", args.plan_name,
        "--runtime", f"PYTHON|{args.python_version}"
    ])

def configure_web_app(args):
    """Configure the Web App"""
    logger.info(f"Configuring Web App: {args.app_name}")
    
    # Set startup command
    run_command([
        "az", "webapp", "config", "set",
        "--name", args.app_name,
        "--resource-group", args.resource_group,
        "--startup-file", f"gunicorn fastapi_server.wsgi:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:{args.port}"
    ])
    
    # Configure environment variables
    run_command([
        "az", "webapp", "config", "appsettings", "set",
        "--name", args.app_name,
        "--resource-group", args.resource_group,
        "--settings", f"WEBSITES_PORT={args.port}"
    ])

def deploy_code(args):
    """Deploy code to Azure using Git"""
    logger.info(f"Setting up Git deployment for: {args.app_name}")
    
    # Configure local Git deployment
    run_command([
        "az", "webapp", "deployment", "source", "config-local-git",
        "--name", args.app_name,
        "--resource-group", args.resource_group
    ])
    
    # Get the Git URL
    result = run_command([
        "az", "webapp", "deployment", "list-publishing-credentials",
        "--name", args.app_name,
        "--resource-group", args.resource_group,
        "--query", "scmUri",
        "--output", "tsv"
    ])
    
    git_url = result.stdout.strip()
    
    logger.info(f"Git deployment URL: {git_url}")
    logger.info("To deploy your code, run the following commands:")
    logger.info(f"  git remote add azure {git_url}")
    logger.info(f"  git push azure main")

def main():
    """Parse arguments and deploy to Azure"""
    parser = argparse.ArgumentParser(description="Deploy TahubuSF FastAPI server to Azure")
    
    parser.add_argument(
        "--app-name",
        type=str, 
        default="TahubuSF",
        help="Azure Web App name (default: TahubuSF)"
    )
    
    parser.add_argument(
        "--resource-group",
        type=str,
        default="TahubuSFResourceGroup",
        help="Azure Resource Group name (default: TahubuSFResourceGroup)"
    )
    
    parser.add_argument(
        "--location",
        type=str,
        default="eastus",
        help="Azure location (default: eastus)"
    )
    
    parser.add_argument(
        "--plan-name",
        type=str,
        default="TahubuSFAppPlan", 
        help="App Service Plan name (default: TahubuSFAppPlan)"
    )
    
    parser.add_argument(
        "--sku",
        type=str,
        default="B1",
        help="App Service Plan SKU (default: B1)"
    )
    
    parser.add_argument(
        "--python-version",
        type=str,
        default="3.10",
        help="Python version (default: 3.10)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for the application (default: 8000)"
    )
    
    parser.add_argument(
        "--steps",
        type=str,
        nargs="+",
        choices=["all", "resource-group", "plan", "webapp", "config", "deploy"],
        default=["all"],
        help="Deployment steps to execute (default: all)"
    )
    
    args = parser.parse_args()
    
    # Check if Azure CLI is installed
    try:
        run_command(["az", "--version"], check=False)
    except FileNotFoundError:
        logger.error("Azure CLI not found. Please install it first.")
        sys.exit(1)
    
    # Check if logged in to Azure
    result = run_command(["az", "account", "show"], check=False)
    if result.returncode != 0:
        logger.warning("Not logged in to Azure. Running 'az login'...")
        run_command(["az", "login"])
    
    # Execute requested steps
    steps = args.steps
    if "all" in steps:
        steps = ["resource-group", "plan", "webapp", "config", "deploy"]
    
    if "resource-group" in steps:
        create_resource_group(args)
    
    if "plan" in steps:
        create_app_service_plan(args)
    
    if "webapp" in steps:
        create_web_app(args)
    
    if "config" in steps:
        configure_web_app(args)
    
    if "deploy" in steps:
        deploy_code(args)
    
    logger.info("Deployment process completed!")
    logger.info(f"Your app will be available at: https://{args.app_name}.azurewebsites.net")

if __name__ == "__main__":
    main() 