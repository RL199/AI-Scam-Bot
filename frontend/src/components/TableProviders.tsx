import {useState, useEffect} from 'react';
import { DataGrid, GridColDef, GridRowSelectionModel} from '@mui/x-data-grid';
import { createTheme, ThemeProvider } from "@mui/material/styles";
import calculateDistance  from '../utils/calculateDistance';
import getProviderHref from '../utils/getProviderHref';
import { CloudAiven } from '../types/types'
import {PostSelectedClouds} from '../api/PostSelectedClouds';

interface CloudListProps {
  clouds: CloudAiven[];
}

const customTheme = createTheme({
  palette: {
    primary: {
    main: '#f00',
    },
  },
});
const columns: GridColDef[] = [
  { field: 'provider_description', headerName: 'Provider Description', flex: 1 },
  { field: 'cloud_name', headerName: 'Cloud Name', flex: 1.5 },
  { field: 'geo_region', headerName: 'Region', flex: 1 },
  { field: 'provider', headerName: 'Provider', flex: 1 },
  { field: 'cloud_description', headerName: 'Cloud Description', flex: 2 },
  { field: 'distance', headerName: 'Distance from you (km)', flex: 1.5, type: 'number' },
{
    field: 'aiven_for_cloud',
    headerName: 'More Info',
    flex: 1,
    renderCell: (params) => {
        const [href, imgSrc] = getProviderHref(params.row.provider);
        const isImage = imgSrc.startsWith('/assets/clouds/');
        return (
            <a href={href} className="flex items-center space-x-2">
          <span>Aiven for</span>
          {isImage && <img src={imgSrc} alt={params.row.provider} style={{ width: 50, height: 30 }} />}
          {!isImage && <span>{params.row.provider}</span>}
        </a>
        );
    }
},
];


export default function TableProviders({ clouds }: CloudListProps) {
  const [userLocation, setUserLocation] = useState<{ lat: number; lon: number } | null>(null);
  const [cloudsWithDistance, setCloudsWithDistance] = useState<CloudAiven[]>([]);
  const [selectedClouds, setSelectedClouds] = useState<string[]>([]);

  useEffect(() => {
    navigator.geolocation.getCurrentPosition((position) => {
      const { latitude, longitude } = position.coords;
      console.log('User location:', latitude, longitude);
      setUserLocation({ lat: latitude, lon: longitude });
    });
  }, []);
  useEffect(() => {
    if (userLocation) {
      const updatedClouds = clouds.map(cloud => ({
        ...cloud,
        distance: calculateDistance(userLocation.lat, userLocation.lon, cloud.geo_latitude, cloud.geo_longitude)
      }));
      setCloudsWithDistance(updatedClouds);
    }
  }, [userLocation, clouds]);



  const handleSelectionChange = (newSelection: GridRowSelectionModel) => {
    // Ensure newSelection is treated as an array and properly type rowId
    const selectedIds = Array.isArray(newSelection) ? newSelection : [];
    setSelectedClouds(selectedIds.map((rowId: string | number) => String(rowId)));
  };

  const handleSubmit = async () => {
    for (const cloud of selectedClouds) {
      const response = await PostSelectedClouds(cloud);
      console.log(response);
      /* maybe develop it in the future */
    }
  };

  return (
    <div className="p-4">
      <ThemeProvider theme={customTheme}>
        <DataGrid

          rows={cloudsWithDistance}
          columns={columns}
          getRowId={(row) => row.cloud_name}
          initialState={{
            pagination: {
              paginationModel: { page: 0, pageSize: 10 },
            },
          }}
          pageSizeOptions={[10, 25, 50, 100]}
          checkboxSelection
          autoHeight
          className="bg-white"
          onRowSelectionModelChange={handleSelectionChange}
          classes={{
            root: 'border-0',
            columnHeader: ' bg-customOrange text-white font-semibold',
            cell: 'text-sm text-left',
            row: 'hover:bg-gray-300',
          }}
        />

        <button onClick={handleSubmit} className="bg-customOrange text-white font-semibold p-2 rounded-md absolute left-4">
          Submit
        </button>
        </ThemeProvider>
    </div>
  );
}
