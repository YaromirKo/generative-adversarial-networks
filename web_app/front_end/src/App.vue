<template>
  <div id="app">
    <b-container fluid>
        <b-col>
            <b-row v-if="show_carousel" align-h="center">
                <h1 style="color:#8B0000;"> Service name </h1>
            </b-row>
            <b-row>
                <carousel-3d
                        v-if="show_carousel"
                        :autoplay="true"
                        :autoplay-timeout="3500"
                        :display="5"
                        :border="1"
                        :clickable="false"
                        class="carousel">
                    <slide v-for="(slide, i) in slides" :index="i" :key="i">
                        <img :src="require('./img/' + `${i + 1}` + '.jpg')">
                    </slide>
                </carousel-3d>
            </b-row>
            <b-row v-if="show_carousel" align-h="center">
              <h5  style="color:#000000;"> Our Web service gives you an opportunity to convert your photo into a piece of art.</h5>
              <h6> You can choose one among provided styles, which will transform your photo into an artist's drawing.For example, select a photo of your doggo (of course, if you have one) and  then  choose the style in which you want to convert your photo of a beautiful creature(doggo.And give some time  to our service to process the photo. </h6>
            </b-row>
            <b-row align-h="center"
              <h5 class="font-weight-bold" v-if="show_carousel" style="color:#000000;"> Our Web service gives you an opportunity to convert your photo into a piece of art. </h5>
              <b-row>
                 </b-row>
             <b-row align-h="center"
              <h6 class="font-weight-bold" v-if="show_carousel" style="color:#000000;"> You can choose one among provided styles, which will transform your photo into an artist's drawing.For example, select a photo of your doggo (of course, if you have one) and  then  choose the style in which you want to convert your photo of a beautiful creature(doggo.And give some time  to our service to process the photo. </h6>
              </b-row>
            <b-row align-h="center">
                <button class="btn_start" v-if="show_carousel" @click="show_carousel = false">START</button>
             </b-row>
        </b-col>
    </b-container>
      <Start v-if="!show_carousel"></Start>
  </div>
</template>

<script>
/* eslint-disable */
import Start from './components/Start.vue'
import axios from 'axios'
import {API} from './main'
import BContainer from "bootstrap-vue/src/components/layout/container"
import BCol from "bootstrap-vue/src/components/layout/col"
import BRow from "bootstrap-vue/src/components/layout/row";
//
export default {
  name: 'app',
  components: {
      BRow,
      Start,
      BCol,
      BContainer
  },
    data() {
      return {
          slides: 5,
          show_carousel: true,
          data: '',
          api: '',
          file: []
    }
  },
    created() {
    },
    mounted() {

    },
    methods: {
        submitFile: function () {
            let formData = new FormData()
            // formData.append("file", this.file)

            for (var i = 0; i < this.file.length; i++) {
                formData.append("file", this.file[i])
            }
            formData.append('id', 179)
            for (var pair of formData.entries()) {
                console.log(pair[0]+ ', ' + pair[1]);
            }
            axios.post(API + '/upload',
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }
            ).then(function (response) {
                console.log(response);
            })
                .catch(function () {
                    console.log('FAILURE!!')
                });
        },

        /*
          Handles a change on the file upload
        */
        handleFileUpload(){
             let uploadedFiles = this.$refs.files.files
            console.log(this.$refs.files.files)

            // this.file = this.$refs.files.files[0];
            for( var i = 0; i < uploadedFiles.length; i++ ){
                this.file.push( uploadedFiles[i] );
            }
        }
    }
}
</script>

<style>
@import url('//fonts.googleapis.com/css?family=Indie+Flower');
#app {
  font-family: 'Indie Flower', cursive;
  text-align: center;
  color: #2c3e50;
}
html, body {
  height: 100vh;
  }
h1 { font-family: "Indie Flower"; font-size: 16px; font-style: normal; font-variant: normal; font-weight: 700; line-height: 17.6px; } h3 { font-family: "Indie Flower"; font-size: 14px; font-style: normal; font-variant: normal; font-weight: 700; line-height: 15.4px; } p { font-family: "Indie Flower"; font-size: 14px; font-style: normal; font-variant: normal; font-weight: 400; line-height: 20px; } blockquote { font-family: "Indie Flower"; font-size: 21px; font-style: normal; font-variant: normal; font-weight: 400; line-height: 30px; } pre { font-family: "Indie Flower"; font-size: 13px; font-style: normal; font-variant: normal; font-weight: 400; line-height: 18.5714px; }

  body {
    margin: 0;
    background: url("./img/background3.jpg") no-repeat center center fixed;
      -webkit-background-size: cover;
      -moz-background-size: cover;
      -o-background-size: cover;
      background-size: cover;
  }
    .btn_start {
        width: 300px;
        /*margin-left: auto;*/
        /*margin-right: auto;*/
        box-sizing: border-box;
        background-color: transparent;
        border: 2px solid #e74c3c;
        border-radius: 0.6em;
        color: #e74c3c;
        cursor: pointer;
        align-self: center;
        font-size: 1rem;
        padding: 1.2em 2.8em;
        text-transform: uppercase;
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
    }
    .btn_start:hover, .btn_start:focus {
        color: #fff;
        outline: 0;
    }
    .btn_start {
        -webkit-transition: box-shadow 300ms ease-in-out, color 300ms ease-in-out;
        transition: box-shadow 300ms ease-in-out, color 300ms ease-in-out;
    }
    .btn_start:hover {
        box-shadow: 0 0 40px 40px #e74c3c inset;
    }
    ::-webkit-scrollbar {
        background-color: gray;
        width: 8px;
    }
    ::-webkit-scrollbar-thumb {
        -webkit-border-radius: 2px;
        border-radius: 2px;
        background-color:#6dc0c8;
    }

</style>
