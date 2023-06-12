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
    people: Object
  },
  data () {
    return {
      cols: ['Building Name', 'Type'],
      people_data: Object.values(this.people),
      rows: [],
      pagination: {
        limit: 5
      }
    }
  },
  created: function () {
    this.people_data.forEach(person => {
      const row = [
        person.first_name,
        person.last_name
      ]
      this.rows.push(row)
    })
  }
}
</script>
