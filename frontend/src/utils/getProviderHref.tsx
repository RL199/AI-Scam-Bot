function getProviderHref(provider: string): [string, string] {
    switch (provider) {
      case 'aws':
        return ['https://aiven.io/aws', '/assets/clouds/aws.png']
      case 'google':
        return ['https://aiven.io/googlecloud', '/assets/clouds/google-cloud.png']
      case 'azure':
        return ['https://aiven.io/azure', '/assets/clouds/azure.png']
      default:
        return ['https://aiven.io', provider]
    }
  }
  
export default getProviderHref