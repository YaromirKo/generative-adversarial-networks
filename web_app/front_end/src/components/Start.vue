<template>
  <b-container fluid class="bv-example-row">
   <b-row align-h="start">
       <b-col cols="" class="left_bar_item mw-100 d-cols-none" :class="{active: index === i}" v-for="(name, i) in names" :key="i" @click="change_content(i)">
            <b-col cols="" align-self="center"><img class="child mw-100" :src="require('../img/' + `${i + 1}` + '.jpg')" alt="456"></b-col>
            <b-col cols="" align-self="center" class="mw-100"><h4 class="">{{name}}</h4></b-col>
       </b-col>
   </b-row>
   <b-row>
       <b-col cols="">
           <b-carousel
                   id="carousel-fade"
                   style=""
                   fade
                   indicators
                   img-width="256"
                   img-height="256">
               <b-carousel-slide
                       v-for="(slide, i) in count"
                       :key="i"
                       caption=""
                       :img-src="require('../img/' + `${index + 1}` + '.jpg')"></b-carousel-slide>
           </b-carousel>
           <!--<carousel-3d-->
                   <!--:autoplay="true"-->
                   <!--:controls-visible="true"-->
                   <!--:perspective="0"-->
                   <!--:autoplay-timeout="3500"-->
                   <!--:display="9"-->
                   <!--:border="1"-->
                   <!--class="carousel">-->
               <!--<slide v-for="(slide, i) in 10" :index="i" :key="i">-->
                   <!--<img class="child" :src="require('../img/' + `${index + 1}` + '.jpg')" alt="456">-->
               <!--</slide>-->
           <!--</carousel-3d>-->
       </b-col>
       <b-col cols="">

       </b-col>
   </b-row>
  </b-container>
</template>

<script>
import BContainer from "bootstrap-vue/src/components/layout/container"
import BCol from "bootstrap-vue/src/components/layout/col"
/* eslint-disable */
import {API} from "../main"
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
          count: 5
      }
    },
    watch: {
    },
    methods: {
      change_content(index) {
          this.index = index
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
