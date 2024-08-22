<script>
    export let targetImage = "/join/placeholder-image2.svg";
    export let fileName = "default";
    
    async function downloadImage() {
    const response = await fetch(targetImage);
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = fileName+"."+targetImage.split('.').pop();
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}
</script>

<img on:click={downloadImage}
              class="tabler-download2"
              style="
                flex-shrink: 0;
                width: 48px;
                height: 48px;
                position: relative;
                overflow: visible;
              "
              src="/join/tabler-download1.svg"
              alt="save"
            />