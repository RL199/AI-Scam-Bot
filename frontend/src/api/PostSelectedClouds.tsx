export const PostSelectedClouds = async (cloud: string) => {
    const response = await fetch('http://127.0.0.1:8000/v1/clouds', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ cloud_name: cloud }),
        });
    
        if (!response.ok) {
            console.log(response);
            throw new Error('Network response was not ok for cloud: ' + cloud);
        }
        
        return response.status;
}