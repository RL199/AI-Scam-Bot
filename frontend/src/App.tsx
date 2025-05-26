import { useState, useEffect} from 'react'
import { CloudAiven } from './types/types';
import { GetCloudProviders } from './api/GetCloudProviders';
import TableProviders from './components/TableProviders'
import './App.css'

function App() {
  const [clouds, setClouds] = useState<CloudAiven[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

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
    <div className='relative p-0 m-0'>
    <div className='flex justify-center items-start relative p-0 m-0'>
        <a className="logo inline-block p-0 m-0 w-[140px] h-[47px] absolute left-4 top-0" href="https://aiven.io">
            <img loading="eager" width="140px" height="47px" src="/assets/logo-aiven.svg" 
            alt="Aiven Logo" />
        </a>
        <h1 className='text-3xl md:text-5xl leading-[1.25] -tracking-[0.02em] font-semibold text-primary whitespace-pre-line text-black'>
          <span className='text-customOrange'> Cloud </span> Providers</h1>
    </div>
    <div>
        <TableProviders clouds={clouds} />
    </div>
    <p className="read-the-docs">
        Click on the Aiven logo to learn more
    </p>
</div>

  )
}

export default App
