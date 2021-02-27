Dropzone.autoDiscover = false;

var app = new Vue({
    el: "#app",
    delimiters: ['[[', ']]'],
    data: {
        dz: null,
        before: null,
        after: null,
        dragCounter: 0,
        loading: false,
        params: {
            threshold_type: 'gaussian',
            threshold_value: 255,
            threshold_inversion: 'none',
            min_fill_area: 20,
            min_path_area: 60,
            stroke_width: 3
        }
    },
    mounted() {
        const $dz = document.getElementById('upload')

        this.dz = new Dropzone('#upload', {
            previewsContainer: ".dropzone-previews",
            paramName: "file", // The name that will be used to transfer the file
            maxFilesize: 2, // MB
            clickable: '.droppable-prompt',
            url: '/',
            autoProcessQueue: false,
            init: function() {
                this.on("addedfile", function(file) { 
                    $dz.classList.remove('drag')
                    $dz.classList.remove('drag')
                    if (this.files.length > 1) {
                        this.removeFile(this.files[0]);
                    }
                    console.log("Added file")
                    app.before = file
                });
                this.on("dragenter", function(event) {
                    event.preventDefault();
                    app.dragCounter++;
                    $dz.classList.add('drag')
                })
                this.on("drop", function(event) {
                    app.dragCounter = 0
                    $dz.classList.remove('drag')
                })
                this.on("dragend", function(event) {
                    $dz.classList.remove('drag')
                })
                this.on("dragleave", function(event) {
                    app.dragCounter--;
                    if (app.dragCounter === 0) { 
                        $dz.classList.remove('drag')
                    }
                })
            },
        });
    },
    methods: {
        downloadSVG() {
            // assuming var `svg` for your SVG node
            var a = document.createElement('a'), xml, ev;
            a.download = `tracey_${this.before.name.replace(/\.[^/.]+$/, "")}.svg`; // file name
            xml = (new XMLSerializer()).serializeToString(this.after); // convert node to xml string
            a.href = 'data:application/octet-stream;base64,' + btoa(xml); // create data uri
            // <a> constructed, simulate mouse click on it
            ev = document.createEvent("MouseEvents");
            ev.initMouseEvent("click", true, false, self, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
            a.dispatchEvent(ev);
        },
        copySVG() {
            var input = document.body.appendChild(document.createElement("input"));
            input.value = document.querySelector('#svg').innerHTML
            input.focus();
            input.select();
            input.setSelectionRange(0, 99999);
            document.execCommand('copy');
            input.parentNode.removeChild(input);
        },
        getSketch() {
            this.loading = true;
            console.log("attempting to get sketch")
            const formData = new FormData();
            formData.append('image', this.dz.getAcceptedFiles()[0]);
        
            const url = '/sketch?' + new URLSearchParams(this.params)

            const options = {
                method: 'POST',
                body: formData,
                // If you add this, upload won't work
                // headers: {
                //   'Content-Type': 'multipart/form-data',
                // }
            };
            fetch(url, options)
            .then(response => response.text())
            .then((response) => {
                r = JSON.parse(response)
                var parser = new DOMParser();
                var doc = parser.parseFromString(r.contents, "image/svg+xml");
                var $el = doc.documentElement
        
                var $svg = document.getElementById("svg")
                while ($svg.firstChild) {
                    $svg.removeChild($svg.firstChild);
                }
                $svg.appendChild($el);

                this.after = $svg

                this.loading = false
            })
            .catch(err => console.log(err))
        }
    }
})
