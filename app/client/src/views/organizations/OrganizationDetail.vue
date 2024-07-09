<template>
  <div class="my_component">
    <div class="card my-2">
      <div class="card-body">
        <h2 class="card-title flex-grow-1"></h2>
        {{ org_data }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.my_component {
    width: 60%;
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
import { CustomRequest } from '../../common/CustomRequest.js'

export default {
  name: 'OrganizationDetail',
  data: function () {
    return {
      id: this.$route.params.id,
      loaded: false,
      org_data: {},
      req: new CustomRequest(this.$cookies.get('session'))
    }
  },
  methods: {
    getOrganization: function () {
      const fetchRequest = window.origin + '/api/v1/organizations?org-id=' + this.id + '&populate=facilities&populate=sales-orders&populate=purchase-orders&populate=people&populate=products'
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
            this.org_data = data.data[0]
            // eslint-disable-next-line
            console.log(this.org_data)
            this.loaded = true
          })
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
    this.getOrganization()
  }
}
</script>
