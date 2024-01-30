<template>
  <div class="my_component">
    <div class="card m-2">
      <div class="card-body">
        <h2 class="card-title flex-grow-1">{{ format_type(component_data.component_type) }} {{ get_comopnent_primary_name(component_data) }}</h2>
      {{ component_data }}
    </div>
    </div>
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
