// script.js
import IpfsMini from 'IpfsMini';

// IpfsMini の定義
const ipfs = new IpfsMini({ host: 'ipfs.infura.io', port: 5001, protocol: 'https' });

document.addEventListener('DOMContentLoaded', (event) => {
  const dropZone = document.getElementById('drop-zone');
  const fileInput = document.getElementById('file-input');
  const uploadButton = document.getElementById('upload-button');
  const ipfsHashContainer = document.getElementById('ipfs-hash');

  dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
  });

  dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
  });

  dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    handleDroppedFiles(e.dataTransfer.files);
  });

  fileInput.addEventListener('change', () => {
    handleSelectedFiles(fileInput.files);
  });

  function handleDroppedFiles(files) {
    displayFileList(files);
  }

  function handleSelectedFiles(files) {
    displayFileList(files);
  }

  function displayFileList(files) {
    const fileListContainer = document.createElement('div');

    Array.from(files).forEach(file => {
      const listItem = document.createElement('div');
      listItem.textContent = file.name;
      fileListContainer.appendChild(listItem);
    });

    document.body.appendChild(fileListContainer);
  }

  // uploadToIPFS 関数の定義
  uploadButton.addEventListener('click', uploadToIPFS);
});

async function uploadToIPFS() {
  const file = document.getElementById('file-input').files[0];

  if (file) {
    const reader = new FileReader();
    reader.onloadend = async function () {
      const fileData = reader.result;
      ipfs.add(fileData, async (err, result) => {
        if (err) {
          console.error(err);
        } else {
          const ipfsHash = result[0].hash;
          // アップロード成功時に IPFS ハッシュを表示
          ipfsHashContainer.textContent = `IPFS Hash: ${ipfsHash}`;
          console.log(`IPFS Hash: ${ipfsHash}`);
        }
      });
    };

    reader.readAsArrayBuffer(file);
  }
}
