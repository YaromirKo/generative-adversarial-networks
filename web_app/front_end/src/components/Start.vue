<template>
  <b-container fluid class="bv-example-row">
   <b-row align-h="start">
     <b-col cols="auto">
       <b-row class="left_bar_item" :class="{active: index === i}" v-for="(name, i) in names" @click="change_content(i)">
        <b-col cols="auto" align-self="center"><img class="child" :src="require('../img/' + `${i + 1}` + '.jpg')" alt="456"></b-col>
        <b-col cols="auto" align-self="center"><h4 class="">{{name}}</h4></b-col>
       </b-row>
     </b-col>
     <b-col>
         <div class="sticky">
             <b-row>
                 <carousel-3d
                         :autoplay="true"
                         :controls-visible="true"
                         :perspective="0"
                         :autoplay-timeout="3500"
                         :display="9"
                         :border="1"
                         class="carousel">
                     <slide v-for="(slide, i) in 10" :index="i">
                         <img class="child" :src="require('../img/' + `${index + 1}` + '.jpg')" alt="456">
                     </slide>
                 </carousel-3d>
             </b-row>
             <b-row>
                 <div class="example-full"  style="width: 100%;">
                     <div v-show="$refs.upload && $refs.upload.dropActive" class="drop-active">
                         <h3>Drop files to upload</h3>
                     </div>
                     <div class="upload" v-show="!isOption">
                         <div class=""  style="height: 500px; overflow-y: auto">
                             <table class="table table-hover">
                                 <thead>
                                 <tr>
                                     <th>#</th>
                                     <th>Picture</th>
                                     <th>Name</th>
                                     <th>Size</th>
                                     <th>Action</th>
                                 </tr>
                                 </thead>
                                 <tbody>
                                 <tr v-if="!files.length">
                                     <td colspan="7">
                                         <div class="text-center p-5">
                                             <h4>Drop files anywhere to upload<br/>or</h4>
                                             <label :for="name" class="btn btn-lg btn-primary">Select Files</label>
                                         </div>
                                     </td>
                                 </tr>
                                 <tr v-for="(file, index) in files" :key="file.id">
                                     <td>{{index}}</td>
                                     <td>
                                         <img v-if="file.thumb" :src="file.thumb" width="40" height="auto" />
                                         <span v-else>No Image</span>
                                     </td>
                                     <td>
                                         <div class="filename">
                                             {{file.name}}
                                         </div>
                                         <div class="progress" v-if="file.active || file.progress !== '0.00'">
                                             <div :class="{'progress-bar': true, 'progress-bar-striped': true, 'bg-danger': file.error, 'progress-bar-animated': file.active}" role="progressbar" :style="{width: file.progress + '%'}">{{file.progress}}%</div>
                                         </div>
                                     </td>
                                     <td>{{file.size}}</td>
                                     <td>
                                         <div class="btn-group">
                                             <button class="btn btn-secondary btn-sm" type="button" @click.prevent="$refs.upload.remove(file)">
                                                 Remove
                                             </button>
                                         </div>
                                     </td>
                                 </tr>
                                 </tbody>
                             </table>
                         </div>
                         <div class="example-foorer">
                             <div class="btn-group">
                                 <file-upload
                                         class="btn btn-primary dropdown-toggle"
                                         :post-action="postAction"
                                         :put-action="putAction"
                                         :extensions="extensions"
                                         :accept="accept"
                                         :multiple="multiple"
                                         :directory="directory"
                                         :size="size || 0"
                                         :thread="thread < 1 ? 1 : (thread > 5 ? 5 : thread)"
                                         :headers="headers"
                                         :data="data"
                                         :drop="drop"
                                         :drop-directory="dropDirectory"
                                         :add-index="addIndex"
                                         v-model="files"
                                         @input-filter="inputFilter"
                                         @input-file="inputFile"
                                         ref="upload">
                                     <i class="fa fa-plus"></i>
                                     Select
                                 </file-upload>
                                 <div class="dropdown-menu">
                                     <label class="dropdown-item" :for="name">Add files</label>
                                     <a class="dropdown-item" href="#" @click="onAddFolader">Add folder</a>
                                     <a class="dropdown-item" href="#" @click.prevent="addData.show = true">Add data</a>
                                 </div>
                             </div>
                             <button type="button" class="btn btn-success" v-if="!$refs.upload || !$refs.upload.active" @click.prevent="$refs.upload.active = true">
                                 <i class="fa fa-arrow-up" aria-hidden="true"></i>
                                 Start Upload
                             </button>
                             <button type="button" class="btn btn-danger"  v-else @click.prevent="$refs.upload.active = false">
                                 <i class="fa fa-stop" aria-hidden="true"></i>
                                 Stop Upload
                             </button>
                         </div>
                     </div>
                 </div>
             </b-row>
         </div>
     </b-col>
   </b-row>
  </b-container>
</template>

<script>
import BContainer from "bootstrap-vue/src/components/layout/container"
import BCol from "bootstrap-vue/src/components/layout/col"
import ImageCompressor from 'image-compressor.js'
export default {
  name: 'Start',
    components: {BCol, BContainer},
    data() {
      return {
          names: [
              'The Starry Night',
              'The Starry Night',
              'The Starry Night',
              'The Starry Night',
              'The Starry Night'
              ],
          index: 0,
          files: [],
          accept: 'image/png,image/gif,image/jpeg,image/webp',
          extensions: 'gif,jpg,jpeg,png,webp',
          // extensions: ['gif', 'jpg', 'jpeg','png', 'webp'],
          // extensions: /\.(gif|jpe?g|png|webp)$/i,
          minSize: 1024,
          size: 1024 * 1024 * 10,
          multiple: true,
          directory: false,
          drop: true,
          dropDirectory: true,
          addIndex: false,
          thread: 3,
          name: 'file',
          postAction: '/upload/post',
          putAction: '/upload/put',
          headers: {
              'X-Csrf-Token': 'xxxx',
          },
          data: {
              '_csrf_token': 'xxxxxx',
          },
          autoCompress: 1024 * 1024,
          uploadAuto: false,
          isOption: false,
          addData: {
              show: false,
              name: '',
              type: '',
              content: '',
          },
          editFile: {
              show: false,
              name: '',
          }
      }
    },
    watch: {
        'editFile.show'(newValue, oldValue) {
            if (!newValue && oldValue) {
                this.$refs.upload.update(this.editFile.id, { error: this.editFile.error || '' })
            }
            if (newValue) {
                this.$nextTick(function () {
                    if (!this.$refs.editImage) {
                        return
                    }
                    let cropper = new Cropper(this.$refs.editImage, {
                        autoCrop: false,
                    })
                    this.editFile = {
                        ...this.editFile,
                        cropper
                    }
                })
            }
        },
        'addData.show'(show) {
            if (show) {
                this.addData.name = ''
                this.addData.type = ''
                this.addData.content = ''
            }
        },
    },
    methods: {
      change_content(index) {
          this.index = index
      },
        inputFilter(newFile, oldFile, prevent) {
            if (newFile && !oldFile) {
                // Before adding a file
                // Filter system files or hide files
                if (/(\/|^)(Thumbs\.db|desktop\.ini|\..+)$/.test(newFile.name)) {
                    return prevent()
                }
                // Filter php html js file
                if (/\.(php5?|html?|jsx?)$/i.test(newFile.name)) {
                    return prevent()
                }
                // Automatic compression
                if (newFile.file && newFile.type.substr(0, 6) === 'image/' && this.autoCompress > 0 && this.autoCompress < newFile.size) {
                    newFile.error = 'compressing'
                    const imageCompressor = new ImageCompressor(null, {
                        convertSize: Infinity,
                        maxWidth: 512,
                        maxHeight: 512,
                    })
                    imageCompressor.compress(newFile.file)
                        .then((file) => {
                            this.$refs.upload.update(newFile, { error: '', file, size: file.size, type: file.type })
                        })
                        .catch((err) => {
                            this.$refs.upload.update(newFile, { error: err.message || 'compress' })
                        })
                }
            }
            if (newFile && (!oldFile || newFile.file !== oldFile.file)) {
                // Create a blob field
                newFile.blob = ''
                let URL = window.URL || window.webkitURL
                if (URL && URL.createObjectURL) {
                    newFile.blob = URL.createObjectURL(newFile.file)
                }
                // Thumbnails
                // 缩略图
                newFile.thumb = ''
                if (newFile.blob && newFile.type.substr(0, 6) === 'image/') {
                    newFile.thumb = newFile.blob
                }
            }
        },
        // add, update, remove File Event
        inputFile(newFile, oldFile) {
            if (newFile && oldFile) {
                // update
                if (newFile.active && !oldFile.active) {
                    // beforeSend
                    // min size
                    if (newFile.size >= 0 && this.minSize > 0 && newFile.size < this.minSize) {
                        this.$refs.upload.update(newFile, { error: 'size' })
                    }
                }
                if (newFile.progress !== oldFile.progress) {
                    // progress
                }
                if (newFile.error && !oldFile.error) {
                    // error
                }
                if (newFile.success && !oldFile.success) {
                    // success
                }
            }
            if (!newFile && oldFile) {
                // remove
                if (oldFile.success && oldFile.response.id) {
                    // $.ajax({
                    //   type: 'DELETE',
                    //   url: '/upload/delete?id=' + oldFile.response.id,
                    // })
                }
            }
            // Automatically activate upload
            if (Boolean(newFile) !== Boolean(oldFile) || oldFile.error !== newFile.error) {
                if (this.uploadAuto && !this.$refs.upload.active) {
                    this.$refs.upload.active = true
                }
            }
        },
        alert(message) {
            alert(message)
        },
        onEditFileShow(file) {
            this.editFile = { ...file, show: true }
            this.$refs.upload.update(file, { error: 'edit' })
        },
        onEditorFile() {
            if (!this.$refs.upload.features.html5) {
                this.alert('Your browser does not support')
                this.editFile.show = false
                return
            }
            let data = {
                name: this.editFile.name,
            }
            if (this.editFile.cropper) {
                let binStr = atob(this.editFile.cropper.getCroppedCanvas().toDataURL(this.editFile.type).split(',')[1])
                let arr = new Uint8Array(binStr.length)
                for (let i = 0; i < binStr.length; i++) {
                    arr[i] = binStr.charCodeAt(i)
                }
                data.file = new File([arr], data.name, { type: this.editFile.type })
                data.size = data.file.size
            }
            this.$refs.upload.update(this.editFile.id, data)
            this.editFile.error = ''
            this.editFile.show = false
        },
        // add folader
        onAddFolader() {
            if (!this.$refs.upload.features.directory) {
                this.alert('Your browser does not support')
                return
            }
            let input = this.$refs.upload.$el.querySelector('input')
            input.directory = true
            input.webkitdirectory = true
            this.directory = true
            input.onclick = null
            input.click()
            input.onclick = (e) => {
                this.directory = false
                input.directory = false
                input.webkitdirectory = false
            }
        },
        onAddData() {
            this.addData.show = false
            if (!this.$refs.upload.features.html5) {
                this.alert('Your browser does not support')
                return
            }
            let file = new window.File([this.addData.content], this.addData.name, {
                type: this.addData.type,
            })
            this.$refs.upload.add(file)
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .left_bar_item {
    margin: 5px;
    border: 1px solid black;
    border-radius: 5px;
    background: rgba(87, 20,0,0.4);
    color: #ffffff;
  }
  .child {
    padding: 5px;
  }

  .child_2 {
    display: inline;
    padding: 50px 10px;
    float: left;
  }
  .text {
    margin-top: 15px;
  }
  .left_bar_item:hover {
    cursor: pointer;
    box-shadow: 0 0 4px 4px #00e708 inset;

  }
  .left_bar_item.active {
    box-shadow: 0 0 4px 4px #00e708 inset;
  }
  .example-full .btn-group .dropdown-menu {
      display: block;
      visibility: hidden;
      transition: all .2s
  }
  .example-full .btn-group:hover > .dropdown-menu {
      visibility: visible;
  }
  .example-full label.dropdown-item {
      margin-bottom: 0;
  }
  .example-full .btn-group .dropdown-toggle {
      margin-right: .6rem
  }
  .example-full .filename {
      margin-bottom: .3rem
  }
  .example-full .btn-is-option {
      margin-top: 0.25rem;
  }
  .example-full .example-foorer {
      padding: .5rem 0;
      border-top: 1px solid #e9ecef;
      border-bottom: 1px solid #e9ecef;
  }
  .example-full .edit-image img {
      max-width: 100%;
  }
  .example-full .edit-image-tool {
      margin-top: .6rem;
  }
  .example-full .edit-image-tool .btn-group{
      margin-right: .6rem;
  }
  .example-full .footer-status {
      padding-top: .4rem;
  }
  .example-full .drop-active {
      top: 0;
      bottom: 0;
      right: 0;
      left: 0;
      opacity: .6;
      text-align: center;
      background: #000;
  }
  .example-full .drop-active h3 {
      margin: -.5em 0 0;
      position: absolute;
      top: 50%;
      left: 0;
      right: 0;
      -webkit-transform: translateY(-50%);
      -ms-transform: translateY(-50%);
      transform: translateY(-50%);
      font-size: 40px;
      color: #fff;
      padding: 0;
  }
    .sticky {
        position: sticky;
        top: 1em;
    }
</style>
