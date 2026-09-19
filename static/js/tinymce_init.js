document.addEventListener("DOMContentLoaded", function() {
    tinymce.init({
        selector: '.tinymce-editor',
        height: 600,
        plugins: 'image link media table code preview',
        toolbar: 'undo redo | bold italic | alignleft aligncenter | image link code',
        relative_urls: false,
		// 指向刚刚开发的后端接口
        images_upload_url: '/upload/image',
        // 选中文件后自动上传
        automatic_uploads: true,
        remove_script_host: true,
		file_picker_callback: function (callback, value, meta) {
            if (meta.filetype === 'file' || meta.filetype === 'media') {
                const input = document.createElement('input');
                input.setAttribute('type', 'file');
        
                input.onchange = function () {
                    const file = this.files[0];
                    const formData = new FormData();
                    formData.append('file', file);
            
                    fetch('/upload/file', { method: 'POST', body: formData })
                    .then(res => res.json())
                    .then(result => {
                        // 将上传成功后的路径与文件名回填至弹窗
                        callback(result.location, { title: result.title });
                    });
                };
            input.click();
            }
        },
    });
});