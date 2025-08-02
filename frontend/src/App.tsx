import { useState, useEffect} from 'react'
import { CloudAiven } from './types/types';
import { GetCloudProviders } from './api/GetCloudProviders';
import TableProviders from './components/TableProviders'
import ChatInterface from './components/ChatInterface'
import { MessageCircle, Cloud } from 'lucide-react'
import './App.css'

function App() {
  const [clouds, setClouds] = useState<CloudAiven[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'clouds' | 'chat'>('clouds');

  useEffect(() => {
    const getCloudData = async () => {
      try {
        const data = await GetCloudProviders();
        setClouds(data);
        
        const providersSet = new Set<string>();
        const geoRegionsSet = new Set<string>();

        data.forEach((cloud) => {
          providersSet.add(cloud.provider_description);
          geoRegionsSet.add(cloud.geo_region);
        });
      } catch (err) {
        setError('Failed to fetch cloud data');
      } finally {
        setLoading(false);
      }
    };

    getCloudData();
  }, []);

  if (loading){
    return <div className='flex flex-col items-center text-black'>
      <img src="/assets/logo-aiven.svg" alt="loading" className='w-30 h-30'/> 
      <p className='font-bold text-xl mt-2'>Loading... </p>
    </div>;
  }
  
  if (error) return <p>{error}</p>;

  return (
    <div className='relative p-0 m-0 h-screen'>
      {/* Header */}
      <div className='flex justify-between items-center p-4 bg-white border-b border-gray-200'>
        <div className='flex items-center space-x-4'>
          <a className="logo inline-block" href="https://aiven.io">
            <img loading="eager" width="140px" height="47px" src="/assets/logo-aiven.svg" 
            alt="Aiven Logo" />
          </a>
          <h1 className='text-2xl font-semibold text-gray-900'>
            IT Support Portal
          </h1>
        </div>
        
        {/* Tab Navigation */}
        <div className='flex space-x-1 bg-gray-100 p-1 rounded-lg'>
          <button
            onClick={() => setActiveTab('clouds')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              activeTab === 'clouds'
                ? 'bg-white text-gray-900 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <Cloud className='w-4 h-4' />
            <span>Cloud Providers</span>
          </button>
          <button
            onClick={() => setActiveTab('chat')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              activeTab === 'chat'
                ? 'bg-white text-gray-900 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <MessageCircle className='w-4 h-4' />
            <span>IT Support Chat</span>
          </button>
        </div>
      </div>

      {/* Content */}
      <div className='h-full'>
        {activeTab === 'clouds' ? (
          <div className='p-6'>
            <div className='mb-6 text-center'>
              <h2 className='text-3xl font-semibold text-gray-900 mb-2'>
                <span className='text-customOrange'>Cloud</span> Providers
              </h2>
              <p className='text-gray-600'>Select and manage your cloud infrastructure</p>
            </div>
            <TableProviders clouds={clouds} />
            <p className="text-sm text-gray-500 text-center mt-6">
              Click on the Aiven logo to learn more
            </p>
          </div>
        ) : (
          <ChatInterface />
        )}
      </div>
    </div>
  )
}

export default App
