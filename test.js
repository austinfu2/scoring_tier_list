// Array of image file names
const imageFileNames = ['image1.jpg', 'image2.jpg', 'image3.jpg', ...];

// Shuffle the array
const shuffledImageFileNames = shuffleArray(imageFileNames);

// Select the first 15 images from the shuffled array
const selectedImages = shuffledImageFileNames.slice(0, 15);

// Loop through the selected images and create HTML elements for each
const imagesDiv = document.getElementById('images');
selectedImages.forEach(imageFileName => {
  const imageElement = document.createElement('img');
  imageElement.setAttribute('src', 'path/to/images/folder/' + imageFileName);
  imageElement.setAttribute('alt', imageFileName);
  imageElement.setAttribute('draggable', 'true');
  imagesDiv.appendChild(imageElement);
});

// Shuffle an array (Fisher-Yates algorithm)
function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}
