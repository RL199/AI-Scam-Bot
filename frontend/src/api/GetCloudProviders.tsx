import { CloudAiven } from '../types/types';

export const GetCloudProviders = async (): Promise<CloudAiven[]> => {
  const response = await fetch('http://127.0.0.1:8000/v1/clouds', {
    method: 'GET'
  });
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }

  const clouds = await response.json();
  return clouds["clouds"];
};