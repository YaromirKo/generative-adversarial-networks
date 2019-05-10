<template>
  <b-container fluid class="bv-example-row">
   <b-row align-h="start">
       <b-col cols="" class="left_bar_item mw-100 d-none d-lg-block d-md-block  d-xl-block" :class="{active: index === i}" v-for="(name, i) in names" :key="i" @click="change_content(i)">
            <b-col cols="" align-self="center"><img class="child mw-100" :src="require('../img/' + `${i + 1}` + '.jpg')" alt="456"></b-col>
            <b-col cols="" align-self="center" class="mw-100"><h4 class="">{{name}}</h4></b-col>
       </b-col>
   </b-row>
   <b-row>
       <b-col cols="12"	sm="6"	md="6"	lg="6"	xl="6">
           <b-carousel id="carousel-fade" fade indicators controls img-width="512" img-height="512" :interval="2000">
               <b-carousel-slide v-for="(slide, i) in paths" :key="i">
                   <img    slot="img"
                           class="img-fluid w-50"
                           :src="url_set(slide['path_input'])"
                           alt="image slot">
                   <img    slot="img"
                           class="img-fluid w-50"
                           :src="url_set(slide['path_target'])"
                           alt="image slot">
               </b-carousel-slide>
           </b-carousel>
       </b-col>
       <b-col cols="12"	sm="6"	md="6"	lg="6"	xl="6">
           <img v-if="preloader" :src="require('../img/preloader.gif')" width="50%" style="border-radius: 8px; " alt="">
           <div v-if="download_url !== null">
               <button @click="download_url = null, files.length = 0">upload again</button>
               <img title="download your stylezed images" width="250px" style="border-radius: 5px; cursor: pointer" @click="downloadItem" :src="require('../img/download.jpg')" alt="download">
           </div>
           <div v-if="!preloader && download_url === null">
               <img style="border-radius: 5px; cursor: pointer; margin-bottom: 5px" title="send images" v-if="files.length !== 0" @click="send" width="100px" :src="require('../img/send.jpg')" alt="">
               <b-form-file placeholder="Chose files" v-if="files.length === 0" v-model="files" accept="image/*" multiple></b-form-file>
               <div v-if="files.length !== 0" style="background-color:rgba(0, 0, 0, 0.2);">
                   <table class="table">
                       <thead>
                           <tr>
                               <th scope="col">img</th>
                               <th scope="col">name</th>
                               <th scope="col">size</th>
                               <th scope="col">delete</th>
                           </tr>
                       </thead>
                       <tbody>
                           <tr v-for="(j, i) in files" class="row_table">
                               <th scope="row"><img width="40px" :src="preview(i)" alt=""></th>
                               <td>{{files[i].name}}</td>
                               <td>{{(files[i].size / 1024).toFixed(2)}} kb</td>
                               <td><span><img title="delete this item" @click="delete_item(i)" width="25px" style="cursor: pointer; border-radius: 13px" :src="require('../img/delete_btn.jpg')"></span></td>
                           </tr>
                       </tbody>
                   </table>
               </div>
           </div>
       </b-col>
   </b-row>
  </b-container>
</template>

<script>
import BContainer from "bootstrap-vue/src/components/layout/container"
import BCol from "bootstrap-vue/src/components/layout/col"
/* eslint-disable */
import {API} from "../main"
import axios from 'axios'
export default {
  name: 'Start',
    components: {
      BCol, BContainer
    },
    data() {
      return {
          names: [
              'The Starry Night',
              'Motif',
              'Scream',
              'Figures At The Seaside',
              'The Great Wave off Kanagawa'
              ],
          index: 0,
          files: [],
          paths: [],
          download_url: null,
          files_length: '',
          type_file: [
              { type: "octet/stream" },
              { zip: 'style_zip.zip' },
              { type: 'image/png' },
              { img: 'style.jpg'}
          ],
          preloader: false,
      }
    },
    watch: {
      index: function () {
          this.get_img_paths(this.index)
      },
    },
    created() {
      this.get_img_paths()
    },
    methods: {
        preview(index) {
            return URL.createObjectURL(this.files[index])
        },
          delete_item(index) {
              this.files.splice(index, 1)
          },
        change_content(index) {
          this.index = index
        },
        downloadItem () {
            axios.get(API + this.download_url, { responseType: 'blob' })
                .then(({ data }) => {
                    let blob = new Blob([data], this.files_length > 1 ? this.type_file[0] : this.type_file[2])
                    let link = document.createElement('a')
                    link.href = URL.createObjectURL(blob)
                    link.download = this.files_length > 1 ? this.type_file[1]['zip'] : this.type_file[3]['img']
                    link.click()
                    this.download_url = ''
                    this.files_length = ''
                })
                .catch(error => {
                    console.error(error)
                })

        },
        send () {
            if (this.files.length !== 0) {
                this.preloader = true

                this.files_length = this.files.length

                let files_pack = new FormData()

                for (let i = 0; i < this.files.length; i++) {
                    console.log(this.files[i])
                    files_pack.append("file", this.files[i])
                }

                files_pack.append("file", files_pack)
                files_pack.append("id_style", this.index)
                for (let pair of files_pack.entries()) {
                    console.log(pair[0] + ', ' + pair[1])
                }

                const headers = {headers: {'Content-Type': 'multipart/form-data'}}

                axios.post(API + '/upload', files_pack, headers)
                    .then((response) => {
                        this.get_img_paths()
                        this.download_url = response.data.link
                        console.log(response)
                        this.preloader = false
                    })
                    .catch((error) => {
                        console.log(error)
                    })
            }
        },
        get_img_paths() {
            axios.get(API + '/get_paths', {
                params: {"id_style" : this.index}
            })
                .then( (response) => {
                    this.paths = response.data.path
                })
                .catch( (error) => {
                    console.log(error)
                })
        },
        url_set(index) {
            return API + index
        }


    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    .row_table:hover {
        background-color: rgba(0, 0, 0, 0.5);
    }
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
