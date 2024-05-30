const [preview, button, output, result] = [    
    document.getElementById('preview'),
    document.getElementById('button'),
    document.getElementById('output'),
    document.getElementById('result'),
]

navigator.mediaDevices.getUserMedia({
    audio: false,
    video: {
        width: 400,
        height: 300,
        facingMode: "environment"
    },
}).then(stream => {
    preview.srcObject = stream;
    preview.play()
}).catch(error => {
    console.log(error)
})

button.addEventListener('click', () => {
    // console.log('works')
    const context = output.getContext('2d');

    output.width = 400;
    output.height = 300;

    context.drawImage(preview, 0, 0, output.width, output.height)
    const image = output.toDataURL("image/jpg", 0,5);

fetch('/detect', {
    method: 'POST',
    body: JSON.stringify({image: image}),
    headers: {
        'Content-Type' : 'application/json'
    }
})
.then(response => {
    if (response.ok) {
        // Periksa tipe konten respons
        const contentType = response.headers.get('content-type');
        
        if (contentType && contentType.includes('application/json')) {
            // Respons adalah JSON, parse dan kembalikan data
            return response.json();
        } else {
            // Respons bukan JSON, tanggapi sesuai kebutuhan
            throw new Error('Invalid content type in response');
        }
    } else {
        // Respons memiliki status kode HTTP yang tidak berhasil
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
})
.then (data => {
    //console.log(data.result_image_base64)
    console.log(data)
    // Mengambil gambar hasil deteksi sebagai basse64 string
    // cont resultImageBase64 = data.result_image_base64;

    // Memasang base64 strinf ke elemen gambar 'result'
    // result.src = 'data:image/jpeg;base64,' + resultImageBase64;
    // result.src = data.result_image_path

    fetch('/detected_image')
    .then(response => response.blob())
    .then(blob => {
        result.src = URL.createObjectURL(blob)
        console.log(result.src)
    })
    .catch ((error) => {
        console.log('Error : ', error)
    })
  
})
})



// capture.addEventListener('click', () => {
//     const context = output.getContext('2d')

//     output.width = 400;
//     output.height = 300;
    
//     context.drawImage(previewVid, 0, 0, output.width, output.height);
//     const image = output.toDataURL("image/jpg", 0.5);

//     fetch('/detect', {
//         method: 'POST',
//         body: JSON.stringify({image: image}),
//         headers: {
//             'Content-Type' : 'application/json'
//         }
//     })
//     .then(response => {
//         if (response.ok) {
//             // Periksa tipe konten respons
//             const contentType = response.headers.get('content-type');
            
//             if (contentType && contentType.includes('application/json')) {
//                 // Respons adalah JSON, parse dan kembalikan data
//                 return response.json();
//             } else {
//                 // Respons bukan JSON, tanggapi sesuai kebutuhan
//                 throw new Error('Invalid content type in response');
//             }
//         } else {
//             // Respons memiliki status kode HTTP yang tidak berhasil
//             throw new Error(`HTTP error! Status: ${response.status}`);
//         }
//     })
//     .then(data => {
//         // console.log(data.result_image_base64)
//         console.log(data)
//         // Mengambil gambar hasil deteksi sebagai base64 string
//         // const resultImageBase64 = data.result_image_base64;

//         // Memasang base64 string ke elemen gambar 'result'
//         // result.src = 'data:image/jpeg;base64,' + resultImageBase64;
//         // result.src = data.result_image_path
        
//         fetch('/detected_image')
//         .then(response => response.blob())
//         .then(blob => {
//             result.src = URL.createObjectURL(blob)
//             console.log(result.src)
//         })
//         .catch((error) => {
//             console.log('Error : ', error)
//         })
//     })

// })