<template>
  <div class="clients">
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
        ':5000' +
        '/organizations'
      )
      fetch('http://' + window.location.hostname + ':5000' + '/organizations', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Credentials': true
        }
      }).then(response => {
        response.json().then(data => {
          this.org_data = data
        })
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
