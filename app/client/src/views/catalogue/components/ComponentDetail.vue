<template>
  <div class="my_component d-flex flex-wrap justify-content-center">
    <div class="card my-2" v-if="!loaded">
      <div class="card-body">
        <div class="d-flex justify-content-center">
          <div class="spinner-border text-primary" role="status"></div>
        </div>
      </div>
    </div>

    <b-container fluid class="p-0">
      <b-card class=" my-2" v-if="loaded">
        <b-card-body>
          <div class="card-title d-flex align-items-center flex-wrap">
            <b-img style="max-width: 15rem;" class="d-none d-print-inline p-2" src="../../../assets/Company Images/logos jpg/Cropped Logo.jpg"></b-img>
            <h2 class="card-title">{{ get_component_primary_name(component_data) }} {{ format_string(component_data.component_type) }}</h2>
            <CertBadge :data="component_data"></CertBadge>
          </div>
          <hr class="d-print-none">
          <b-nav pills card-header slot="header" v-b-scrollspy:nav-scroller class="text-nowrap d-print-none">
            <b-nav-item href="#Aliases" @click="scrollIntoView">Aliases</b-nav-item>
            <b-nav-item href="#Specifications" @click="scrollIntoView"
              v-if="component_data.doc.specifications !== undefined">Specifications</b-nav-item>
            <div v-for="(spec, spec_key) in component_data.doc.specifications.specs" :key="spec_key">
              <b-nav-item :href="'#'+spec_key" @click="scrollIntoView">{{ spec.test_name }}</b-nav-item>
            </div>
          </b-nav>
        </b-card-body>
      </b-card>

      <b-card class=" my-2" v-if="loaded">
        <b-card-body id="nav-scroller" ref="content" class="scrollbox">

          <!-- Alias Names -->
          <NamesComponent
            :p-names="component_data.component_names"
            :id="component_data.component_id"
            naming-type="component"
            :allow-edit="true"
            v-on:edit-names="(e) => edit_names = e"
            v-on:toggle-loaded="toggleLoaded"
            v-on:refresh-parent="refreshParent"
          ></NamesComponent>
          <hr>

          <!-- Specifications -->
          <SpecificationsComponent
            :doc="component_data.doc"
            :spectype="'component'"
            :name="get_component_primary_name(component_data)"
            :id="component_data.component_id"
            v-on:edit-specs="(e) => edit_specs = e"
            v-on:toggle-loaded="toggleLoaded"
            v-on:refresh-parent="(v) => refreshParent(v)"
          ></SpecificationsComponent>

        </b-card-body>
      </b-card>
    </b-container>
  </div>
</template>

<style scoped>
.scrollbox {
  position:relative;
  height:85vh;
  overflow-y:scroll;
}
.customize-table {
  --easy-table-body-item-padding:10px 10px 10px 10px;
}
@media print {
  .scrollbox {
    height: 100%;
    overflow-y:auto;
  }
  @page {
    margin: 30mm 30mm 10mm 10mm;
  }
  body {
    margin: 0px;
  }
}
.bold {
    font-weight: bold;
}
.my_component {
    width: 95%;
}
@media (max-width: 1024px) {
    .my_component {
        width: 98%;
    }
}
@media (max-width: 400px) {
    .my_component {
        width: 100%;
    }
}
</style>

<script>
import NamesComponent from './NamesComponent.vue'
import CertBadge from '../../../components/CertBadge.vue'
import SpecificationsComponent from '../SpecificationsComponent.vue'

export default {
  name: 'ComponentDetail',
  components: {
    NamesComponent,
    CertBadge,
    SpecificationsComponent
  },
  data: function () {
    return {
      id: this.$route.params.id,
      component_data: {},
      loaded: false,
      edit_names: false,
      edit_specs: false
    }
  },
  methods: {
    toggleLoaded: function (val) {
      this.loaded = val
    },
    refreshParent: function (val) {
      this.getComponentData()
    },
    scrollIntoView: function (event) {
      event.preventDefault()
      const href = event.target.getAttribute('href')
      const el = href ? document.querySelector(href) : null
      if (el) {
        this.$refs.content.scrollTop = el.offsetTop
      }
    },
    format_string: function (type) {
      if (type === undefined) {
        return ''
      }
      return type.toLowerCase().split('_').map((s) => s.charAt(0).toUpperCase() + s.substring(1)).join(' ')
    },
    get_component_primary_name: function (component) {
      if (component.component_names !== undefined && component.component_names.length > 0) {
        for (let i = 0; i < component.component_names.length; i++) {
          if (component.component_names[i].primary_name) {
            return component.component_names[i].component_name
          }
        }
      }
      return 'No Name'
    },
    getComponentData: function () {
      const fetchRequest = window.origin + '/api/v1/catalogue/components?component-id=' + this.id + '&populate=component_names&doc=true'
      // eslint-disable-next-line
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
            this.component_data = data.data[0]
            if (this.component_data.doc === null) {
              this.component_data.doc = {}
            }
            // eslint-disable-next-line
            console.log(this.component_data)
            this.loaded = true
          })
        } else if (response.status === 404) {
          this.$router.push({ path: '/404' })
        } else if (response.status === 401) {
          this.$router.push({
            name: 'login'
          })
        } else {
          // eslint-disable-next-line
          console.log('Looks like there was a problem. Status Code:' + response.status)
          // eslint-disable-next-line
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
