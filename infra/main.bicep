// Deploying Azure Functions App to Azure
//
// Author: Bernhard Flür
// Date: 17-03-2023
// Version: 1.0

// Define parameters
param AppName string
param location string = resourceGroup().location
param Schedule string = '0 0 3 * * *'

@description('The id of the Azure billing account to use for billing.')
param BillingAccountId string


// Define variables
var storageAccountName = '${uniqueString(resourceGroup().id)}azfunctions'
var storageAccountType = 'Standard_LRS'
var FunctionAppName = AppName
var HostPlanName = '${AppName}-plan'
var appInsightsName = '${AppName}-Insights'


// Define resources
resource storageAccount 'Microsoft.Storage/storageAccounts@2022-09-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: storageAccountType
  }
  kind: 'StorageV2'
}

resource hostPlan 'Microsoft.Web/serverfarms@2022-09-01' = {
  name: HostPlanName
  location: location
  kind: 'linux'
  sku: {
    name: 'S1'
  }
  properties: {
    reserved: true
  }
}

resource insightsComponents 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
  }
}

resource azureFunctionApp 'Microsoft.Web/sites@2022-09-01' = {
  name: FunctionAppName
  location: location
  kind: 'functionapp,linux'
  properties: {
    serverFarmId: hostPlan.id
    siteConfig: {
      alwaysOn: true
      linuxFxVersion: 'Python|3.10'
      appSettings: [
        {
          name: 'AzureWebJobsDashboard'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};EndpointSuffix=${environment().suffixes.storage};AccountKey=${storageAccount.listKeys().keys[0].value}'
        }
        {
          name: 'AzureWebJobsStorage'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};EndpointSuffix=${environment().suffixes.storage};AccountKey=${storageAccount.listKeys().keys[0].value}'
        }
        {
          name: 'WEBSITE_CONTENTAZUREFILECONNECTIONSTRING'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};EndpointSuffix=${environment().suffixes.storage};AccountKey=${storageAccount.listKeys().keys[0].value}'
        }
        {
          name: 'WEBSITE_CONTENTSHARE'
          value: toLower(AppName)
        }
        {
          name: 'Schedule'
          value: Schedule
        }
        {
          name: 'BILLING_ACCOUNT_ID'
          value: BillingAccountId
        }
        {
          name: 'FUNCTIONS_EXTENSION_VERSION'
          value: '~4'
        }
        {
          name: 'APPINSIGHTS_INSTRUMENTATIONKEY'
          value: insightsComponents.properties.InstrumentationKey
        }
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'python'
        }
      ]
    }
    httpsOnly: true
  }
  identity: {
    type: 'SystemAssigned'
  }
}
