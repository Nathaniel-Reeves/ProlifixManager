<template>
  <div class="my_component d-flex flex-wrap justify-content-center">
    <div class="card m-2 p-2" v-show="!loaded">
      <div class="card-body">
        <div class="d-flex justify-content-center">
          <div class="spinner-border text-primary" role="status"></div>
        </div>
      </div>
    </div>

    <b-container fluid>
      <b-card class="m-2" v-show="loaded">
        <b-card-body>
          <h2 class="card-title">{{ format_type(component_data.component_type) }} {{ get_comopnent_primary_name(component_data) }}</h2>
          <hr>
          <b-nav pills card-header slot="header" v-b-scrollspy:nav-scroller class="text-nowrap">
            <b-nav-item href="#Description" @click="scrollIntoView">Description</b-nav-item>
            <b-nav-item href="#Aliases" @click="scrollIntoView">Aliases</b-nav-item>
            <b-nav-item href="#Specifications" @click="scrollIntoView">Specifications</b-nav-item>
            <b-nav-item href="#Sources" @click="scrollIntoView">Sources</b-nav-item>
          </b-nav>
        </b-card-body>
      </b-card>

      <b-card class="m-2" v-show="loaded">
        <b-card-body id="nav-scroller" ref="content" style="position:relative; height:60vh; overflow-y:scroll;">
          <h3 id="Description">Description</h3>
          <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Libero justo laoreet sit amet cursus sit amet. Et ultrices neque ornare aenean euismod elementum. Amet dictum sit amet justo donec enim diam vulputate. Est ultricies integer quis auctor elit. Habitasse platea dictumst quisque sagittis. Nulla malesuada pellentesque elit eget gravida cum sociis natoque penatibus. Ligula ullamcorper malesuada proin libero. Dictum varius duis at consectetur lorem donec massa. Eu turpis egestas pretium aenean pharetra magna ac placerat. Auctor neque vitae tempus quam pellentesque nec. Commodo elit at imperdiet dui accumsan sit amet nulla. Nulla facilisi nullam vehicula ipsum a arcu cursus vitae congue. Ultrices gravida dictum fusce ut placerat orci. Luctus venenatis lectus magna fringilla urna porttitor rhoncus dolor purus. Faucibus turpis in eu mi bibendum neque egestas congue. Cras semper auctor neque vitae tempus quam pellentesque. Turpis egestas pretium aenean pharetra magna. Euismod nisi porta lorem mollis aliquam ut porttitor leo.</p>
          <h3 id="Aliases">Aliases</h3>
          <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Libero justo laoreet sit amet cursus sit amet. Et ultrices neque ornare aenean euismod elementum. Amet dictum sit amet justo donec enim diam vulputate. Est ultricies integer quis auctor elit. Habitasse platea dictumst quisque sagittis. Nulla malesuada pellentesque elit eget gravida cum sociis natoque penatibus. Ligula ullamcorper malesuada proin libero. Dictum varius duis at consectetur lorem donec massa. Eu turpis egestas pretium aenean pharetra magna ac placerat. Auctor neque vitae tempus quam pellentesque nec. Commodo elit at imperdiet dui accumsan sit amet nulla. Nulla facilisi nullam vehicula ipsum a arcu cursus vitae congue. Ultrices gravida dictum fusce ut placerat orci. Luctus venenatis lectus magna fringilla urna porttitor rhoncus dolor purus. Faucibus turpis in eu mi bibendum neque egestas congue. Cras semper auctor neque vitae tempus quam pellentesque. Turpis egestas pretium aenean pharetra magna. Euismod nisi porta lorem mollis aliquam ut porttitor leo.</p>
          <h3 id="Specifications">Specifications</h3>
          <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Libero justo laoreet sit amet cursus sit amet. Et ultrices neque ornare aenean euismod elementum. Amet dictum sit amet justo donec enim diam vulputate. Est ultricies integer quis auctor elit. Habitasse platea dictumst quisque sagittis. Nulla malesuada pellentesque elit eget gravida cum sociis natoque penatibus. Ligula ullamcorper malesuada proin libero. Dictum varius duis at consectetur lorem donec massa. Eu turpis egestas pretium aenean pharetra magna ac placerat. Auctor neque vitae tempus quam pellentesque nec. Commodo elit at imperdiet dui accumsan sit amet nulla. Nulla facilisi nullam vehicula ipsum a arcu cursus vitae congue. Ultrices gravida dictum fusce ut placerat orci. Luctus venenatis lectus magna fringilla urna porttitor rhoncus dolor purus. Faucibus turpis in eu mi bibendum neque egestas congue. Cras semper auctor neque vitae tempus quam pellentesque. Turpis egestas pretium aenean pharetra magna. Euismod nisi porta lorem mollis aliquam ut porttitor leo.</p>
          <h3 id="Sources">Sources</h3>
          <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Libero justo laoreet sit amet cursus sit amet. Et ultrices neque ornare aenean euismod elementum. Amet dictum sit amet justo donec enim diam vulputate. Est ultricies integer quis auctor elit. Habitasse platea dictumst quisque sagittis. Nulla malesuada pellentesque elit eget gravida cum sociis natoque penatibus. Ligula ullamcorper malesuada proin libero. Dictum varius duis at consectetur lorem donec massa. Eu turpis egestas pretium aenean pharetra magna ac placerat. Auctor neque vitae tempus quam pellentesque nec. Commodo elit at imperdiet dui accumsan sit amet nulla. Nulla facilisi nullam vehicula ipsum a arcu cursus vitae congue. Ultrices gravida dictum fusce ut placerat orci. Luctus venenatis lectus magna fringilla urna porttitor rhoncus dolor purus. Faucibus turpis in eu mi bibendum neque egestas congue. Cras semper auctor neque vitae tempus quam pellentesque. Turpis egestas pretium aenean pharetra magna. Euismod nisi porta lorem mollis aliquam ut porttitor leo.</p>
          {{ component_data }}
        </b-card-body>
      </b-card>
    </b-container>
  </div>
</template>

<style scoped>
.my_component {
    width: 95%;
}
</style>

<script>
export default {
  name: 'ComponentDetail',
  data: function () {
    return {
      id: this.$route.params.id,
      component_data: {},
      search_query: '',
      loaded: false
    }
  },
  methods: {
    scrollIntoView: function (event) {
      event.preventDefault()
      const href = event.target.getAttribute('href')
      const el = href ? document.querySelector(href) : null
      if (el) {
        this.$refs.content.scrollTop = el.offsetTop
      }
    },
    format_type: function (type) {
      if (type === undefined) {
        return ''
      }
      return type.toLowerCase().split('_').map((s) => s.charAt(0).toUpperCase() + s.substring(1)).join(' ')
    },
    get_comopnent_primary_name: function (component) {
      if (component.Component_Names !== undefined && component.Component_Names.length > 0) {
        for (let i = 0; i < component.Component_Names.length; i++) {
          if (component.Component_Names[i].primary_name) {
            return component.Component_Names[i].component_name
          }
        }
      }
      return 'No Name'
    },
    get_component_brand_name: function (component) {
      if (component.Organization_Names !== undefined && component.Organization_Names.length > 0) {
        for (let i = 0; i < component.Organization_Names.length; i++) {
          if (component.Organization_Names[i].primary_name) {
            return component.Organization_Names[i].organization_name
          }
        }
      }
      return ''
    },
    getComponentData: function () {
      const fetchRequest = window.origin + '/api/v1/catalogue/components?component-id=' + this.id + '&populate=product_materials&populate=purchase_order_detail&populate=label_formula_master&populate=ingredient_formula_master&populate=item_id&populate=inventory&populate=brand&doc=true'
      console.log(
        'GET ' + fetchRequest
      )
      fetch(fetchRequest, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include'
      }).then(response => {
        if (response.status === 200) {
          response.json().then(data => {
            this.component_data = Object.values(data.data[0])[0]
            console.log(this.component_data)
            this.loaded = true
          })
        } else if (response.status === 401) {
          this.$router.push({
            name: 'login'
          })
        } else {
          console.log('Looks like there was a problem. Status Code:' + response.status)
          console.log(response)
        }
      })
    }
  },
  created: function () {
    this.getComponentData()
  }
}
</script>
