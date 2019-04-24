import Vue from 'vue'
import App from './App.vue'
import BootstrapVue from 'bootstrap-vue'

import Carousel3d  from 'vue-carousel-3d'
import Slide from 'vue-carousel-3d'

Vue.use(Carousel3d)
Vue.use(Slide)
Vue.use(BootstrapVue)


import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

export const API =  'http://127.0.0.1:5000'

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
