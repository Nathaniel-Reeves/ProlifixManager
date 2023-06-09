<template>
  <div class="clients">
    <div class="accordion" id="accordionExample">

      <div class="card" v-for="org in org_data" :key="org.organization_id">
        <div class="card-header" v-bind:id="'heading' + org.organization_id">
          <h2 class="mb-0">
            <button class="btn btn-link btn-block text-left" type="button" data-toggle="collapse" v-bind:data-target="'#collapse' + org.organization_id" aria-expanded="false" v-bind:aria-controls="'collapse' + org.organization_id">
              {{ org.organization_name }}
            </button>
          </h2>
        </div>

        <div v-bind:id="'collapse' + org.organization_id" class="collapse" v-bind:aria-labelledby="'heading' + org.organization_id" data-parent="#accordionExample">
          <div class="card-body">
            <ProductsGrid v-bind:products="org.products"></ProductsGrid>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import ProductsGrid from '../../components/ProductsGrid.vue'

export default {
  name: 'ClientsOrg',
  data: function () {
    return {
      org_data: []
    }
  },
  methods: {
    getOrgData: function () {
      var fetchRequest = window.origin + '/api/organizations?org-type=client&populate=products'
      console.log(
        'GET ' + fetchRequest
      )
      fetch(fetchRequest, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
      }).then(response => {
        if (response.status === 200) {
          response.json().then(data => {
            this.org_data = data
          })
        } else {
          console.log('Looks like there was a problem. Status Code:' + response.status)
          console.log(response)
        }
      })
    }
  },
  created: function () {
    this.getOrgData()
  },
  props: {
    msg: String
  },
  components: {
    ProductsGrid
  }
}
</script>
