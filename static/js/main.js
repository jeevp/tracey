Dropzone.autoDiscover = false

var app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {
    dz: null,
    ds: null,
    info: false,
    before: null,
    dragCounter: 0,
    numPaths: 0,
    loading: false,
    params: {
      trace_type: 'threshold',
      threshold_type: 'binary',
      threshold_value: 40,
      min_edge_value: 100,
      max_edge_value: 200,
      min_path_area: 10,
      max_path_area: 80,
      path_complexity: 2,
      stroke_width: 4,
      roundness: 1,
    },
    result: null,
  },
  mounted() {
    window.addEventListener('keydown', function (e) {
      if (e.keyCode == 8 && app.ds.getSelection().length) {
        app.deletePaths()
      }
    })
    const $dz = document.getElementById('upload')
    this.dz = new Dropzone('#upload', {
      previewsContainer: '.dropzone-previews',
      paramName: 'file', // The name that will be used to transfer the file
      maxFilesize: 2, // MB
      clickable: '.droppable-prompt',
      url: '/',
      autoProcessQueue: false,
      init: function () {
        this.on('addedfile', function (file) {
          $dz.classList.remove('drag')
          $dz.classList.remove('drag')
          if (this.files.length > 1) {
            this.removeFile(this.files[0])
          }
          app.before = file
        })
        this.on('dragenter', function (event) {
          event.preventDefault()
          app.dragCounter++
          $dz.classList.add('drag')
        })
        this.on('drop', function (event) {
          app.dragCounter = 0
          $dz.classList.remove('drag')
        })
        this.on('dragend', function (event) {
          $dz.classList.remove('drag')
        })
        this.on('dragleave', function (event) {
          app.dragCounter--
          if (app.dragCounter === 0) {
            $dz.classList.remove('drag')
          }
        })
      },
    })
  },
  methods: {
    getSketch() {
      this.loading = true
      const formData = new FormData()
      formData.append('image', this.dz.getAcceptedFiles()[0])
      const url = '/paths?' + new URLSearchParams(this.params)
      const options = {
        method: 'POST',
        body: formData,
      }
      fetch(url, options)
        .then((response) => response.text())
        .then((response) => {
          this.result = JSON.parse(response)
          this.loading = false
          this.$nextTick(() => {
            this.renderSketch()
          })
        })
        .catch((err) => {
          console.log(err)
          alert(
            'Oops, something went wrong... please reload the page and try again.'
          )
          this.loading = false
        })
    },
    renderSketch() {
      if (!this.$refs.tracey) return false
      this.$refs.tracey.setAttribute(
        'viewBox',
        `0 0 ${this.result.dimensions.width} ${this.result.dimensions.height}`
      )
      this.$refs.tracey.setAttribute('width', this.result.dimensions.width)
      this.$refs.tracey.setAttribute('height', this.result.dimensions.height)
      var $svgContainer = document.querySelector('#tracey')
      this.ds = new DragSelect({
        selectables: document.getElementsByTagName('path'),
        area: $svgContainer,
      })
      var $paths = document.getElementsByTagName('path')
      for (let i = 0; i < $paths.length; i++) {
        const $path = $paths[i]
        var length = Math.ceil($path.getTotalLength()) + 1
        $path.setAttribute('stroke-dasharray', length)
        $path.setAttribute('stroke-dashoffset', length)
      }
      this.numPaths = $paths.length
    },
    deletePaths() {
      let selected = this.ds.getSelection()
      for (let i = 0; i < selected.length; i++) {
        const $el = selected[i]
        $el.remove()
        this.numPaths--
      }
    },
    getSpline(pts) {
      const k = this.params.roundness
      if (k == 0) return pts
      let p0 = [],
        [p1, p2, p3] = pts
      const path = [p1]
      for (let i = 1, len = pts.length; i < len - 1; i++) {
        p0 = p1
        p1 = p2
        p2 = p3
        p3 = pts[i + 2] ? pts[i + 2] : p2
        path.push([
          p1[0] + ((p2[0] - p0[0]) / 6) * k,
          p1[1] + ((p2[1] - p0[1]) / 6) * k,
          p2[0] - ((p3[0] - p1[0]) / 6) * k,
          p2[1] - ((p3[1] - p1[1]) / 6) * k,
          p2[0],
          p2[1],
        ])
      }
      return path
    },
    pathToString(arr) {
      if (this.params.roundness > 0) {
        let flat = arr.flat()
        let mPoints = flat.slice(0, 2)
        let cPoints = flat.slice(2)
        return `M ${mPoints.join(' ')} C ${cPoints.join(' ')}`
      } else {
        return `M ${arr.flat().join(' ')}`
      }
    },
    copySVG() {
      var input = document.body.appendChild(document.createElement('input'))
      input.value = document.querySelector('#svg').innerHTML
      input.focus()
      input.select()
      input.setSelectionRange(0, 99999)
      document.execCommand('copy')
      input.parentNode.removeChild(input)
    },
    downloadSVG() {
      // assuming var `svg` for your SVG node
      var a = document.createElement('a'),
        xml,
        ev
      a.download = `tracey_${this.before.name.replace(/\.[^/.]+$/, '')}.svg` // file name
      xml = new XMLSerializer().serializeToString(this.$refs.tracey) // convert node to xml string
      a.href = 'data:application/octet-stream;base64,' + btoa(xml) // create data uri
      // <a> constructed, simulate mouse click on it
      ev = document.createEvent('MouseEvents')
      ev.initMouseEvent(
        'click',
        true,
        false,
        self,
        0,
        0,
        0,
        0,
        0,
        false,
        false,
        false,
        false,
        0,
        null
      )
      a.dispatchEvent(ev)
    },
  },
})
