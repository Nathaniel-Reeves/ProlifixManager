<template>
    <Grid :cols="cols" :rows="rows" :pagination="{'limit':5}" :sort="true"></Grid>
</template>

<script>
import Grid from 'gridjs-vue'

export default {
  name: 'PeopleGrid',
  components: {
    Grid
  },
  props: {
    People: Array
  },
  data () {
    return {
      cols: ['First Name', 'Last Name'],
      people_data: this.People,
      rows: [],
      pagination: {
        limit: 5
      }
    }
  },
  created: function () {
    if (this.people_data !== undefined) {
      this.people_data.forEach(person => {
        const row = [
          person.first_name,
          person.last_name
        ]
        this.rows.push(row)
      })
    }
  }
}
</script>
