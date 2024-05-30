const dropArea = document.getElementById("drop-area");
const inputFile = document.getElementById("input-file");
const imageView = document.getElementById("img-view");
const resultImage = document.getElementById("result");

// Fungsi untuk menampilkan gambar yang di drop
function uploadImage(file) {
    //Set background image untuk imageView
    const imgLink = URL.createObjectURL(file); //Dapaatkan URL gambar
    imageView.style.backgroundImage = `url(${imgLink})`;
    imageView.textContent = "";
    imageView.style.border = 0;

    // Membuat objek FormData untuk mengirim gambar ke server
    const formData = new FormData();
    formData.append('image', file); //Gunakan file yang dipilih sebagai datayang dikirim

    // Mengirim permintaan POST ke endpoint '/foto_galeri'
    fetch('/foto_galeri', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Failed to process image');
        }
    })
    .then(data => {
        console.log(data);
        //Menampilkan hasil gambar deteksi
        resultImage.src = '/Static/Images/' + data.result_image_path;
        updateResultImage();

    })
    .catch(error => {
        console.error('Error:', error);
        //Menampilkan pesar error
        resultImage.src = 'error.png'; // Ganti dengan gambar error yang seuai
    })
}

function updateResultImage() {
    fetch('/detected_image') // Ubah URL ini sesuai dengan endpoint Anda untuk mendapatkan hasil deteksi terbaru
    .then(response => {
        if (response.ok) {
            return response.blob();
        } else {
            throw new Error('Failed to fetch updated image');
        }
    })
    .then(blob => {
        resultImage.src = URL.createObjectURL(blob);
        console.log(result.src);
    })
    .catch(error => {
        console.log('Error:', error);
        result.src = 'error.png'; //Ganti dengan gambar error yang sesuai
    });
}

// Mengabaikan peristiwa default untuk drag and drop
dropArea.addEventListener("dragover", function(e){
    e.preventDefault();
});
dropArea.addEventListener("drop", function(e){
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) {
        uploadImage(file); //Panggil fungsi uploadImage dengan file sebagai argumen
    }
});

// Menangani peristiwa saat file dipilih menggunakan input file
inputFile.addEventListener("change", function() {
    const file = inputFile.files[0];
    if (file) {
        uploadImage(file); //Panggil fungsi uploadImage dengan file sebagai argumen
    }
});

// Menangani peristiwa klik pada tombol "Predict"
document.querySelector('.button'). addEventListener('click', function() {
    const file = inputFile.files[0];
    if (file) {
        uploadImage(file); //Panggil fungsi uploadImage dengan file sebagai argumen
    }
});