<template>
  <div class="clients">
    <p>{{ org_data.message }}</p>
    <div v-for="org in org_data" :key="org.id">
      <p>{{ org.organization_name }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ClientsOrg',
  data: function () {
    return {
      org_data: []
    }
  },
  methods: {
    getOrgData: function () {
      console.log(
        'GET ' +
        window.location.hostname +
        ':8080' +
        '/api/organizations/test'
      )
      fetch('http://' + window.location.hostname + ':8080' + '/api/organizations/test', {
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
  }
}
</script>
