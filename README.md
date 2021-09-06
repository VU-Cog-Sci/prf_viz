# pRF parameter and interactive time-course visualisation on a HCP 59k flatmap

The idea here is to visualize some voxelwise modeling result on a flatmap. This flatmap is an object that you can click, which then updates a time-course (or any other) figure based on the clicked vertex. This greatly enhances one's ability to quickly iterate, and gain intuition for some dataset. 

### Just look:

https://user-images.githubusercontent.com/436593/132212568-ed9d3333-7e30-4f0f-9090-28abbe230ebd.mov

### Requisite data files:

The required gifti files for the time-courses and fitting results (limited to V1 and V2 for this demo) are in the `data` folder. The pycortex subject that we use here can be downloaded from figshare, and should be unzipped into your pycortex subject directory, as follows (change db directory):

```
pycortex_sj_URL = "https://ndownloader.figshare.com/files/25768841"

urllib.request.urlretrieve(pycortex_sj_URL, os.path.join('/content/pycortex/db', 'hcp_999999.zip'))
!unzip -qq /content/pycortex/db/hcp_999999.zip -d /content/pycortex/db/
```
