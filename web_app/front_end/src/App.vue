<template>
  <div id="app">
    <carousel-3d
            v-if="show_carousel"
            :autoplay="true"
            :autoplay-timeout="3500"
            :display="5"
            :border="1"
            class="carousel">
        <slide v-for="(slide, i) in slides" :index="i">
            <img :src="require('./img/' + `${i + 1}` + '.jpg')">
        </slide>
    </carousel-3d>
     <h1 v-if="show_carousel">Welcome</h1>
     <button class="btn_start" v-if="show_carousel" @click="show_carousel = false">START</button>
     <Start v-if="!show_carousel"></Start>
  </div>
</template>

<script>
import Start from './components/Start.vue'
import axios from 'axios'
import {API} from './main'

export default {
  name: 'app',
  components: {
      Start
  },
    data() {
      return {
          slides: 5,
          show_carousel: true,
          data: ''
    }
  },
    mounted() {
    },
    methods: {
      test_flask() {
          axios.get(API)
              .then(response => {
                  this.data = response.data
                  console.log(response)
              })
              .catch(error => {
                  console.log('error')
              })

      }
    }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
  body {
    height: 100%;
    margin: 0;
    /*background: linear-gradient(to right top, #ffc171, #ffb280, #ffa695, #ff9ead, #ff9cc4, #f4a3db, #e3acef, #ccb6ff, #a1c5ff, #6ad3ff, #30dfff, #26e7f0) no-repeat fixed;*/
      background: url("./img/background3.jpg") no-repeat fixed center;
      background-size: cover;
  }
    .btn_start {
        width: 300px;
        margin-left: auto;
        margin-right: auto;
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
