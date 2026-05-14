terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_storage_account" "shopflow_data" {
  name                     = "shopflowdevsecops"
  resource_group_name      = "ShopFlow-RG"
  location                 = "eastus"
  account_tier             = "Standard"
  account_replication_type = "LRS"

  # VULN-9: Public blob access — anyone on the internet can read blobs
  # Checkov: CKV_AZURE_59
  allow_nested_items_to_be_public = true

  # VULN-10: HTTP allowed — data in transit unencrypted
  # Checkov: CKV_AZURE_3
  enable_https_traffic_only = false

  # Missing: min_tls_version — defaults to TLS1_0
  # Checkov: CKV_AZURE_44

  # Missing: blob_properties soft_delete_policy
  # Checkov: CKV_AZURE_111
}

resource "azurerm_storage_container" "uploads" {
  name                  = "uploads"
  storage_account_name  = azurerm_storage_account.shopflow_data.name
  # VULN-11: blob access level public — bypasses authentication entirely
  # Checkov: CKV2_AZURE_21
  container_access_type = "blob"
}