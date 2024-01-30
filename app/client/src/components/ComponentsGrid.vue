<template>
    <Grid :cols="cols" :rows="rows" :pagination="{'limit':5}" :sort="true"></Grid>
</template>

<style scoped>
.custom-button {
  border-width: 2px;
  border-color: #999999;
}
</style>

<script>
import { h } from 'gridjs'
import Grid from 'gridjs-vue'

export default {
  name: 'ComponentsGrid',
  components: {
    Grid
  },
  props: {
    Components: Array,
    Component_Names: Array
  },
  data () {
    return {
      cols: [
        {
          name: 'id',
          hidden: true
        },
        {
          name: 'Name'
        },
        {
          name: 'Type'
        },
        {
          name: 'Actions',
          formatter: (cell, row) => {
            return h('button', {
              className: 'btn .custom-button rounded-pill btn-light',
              onClick: () => this.view_row(cell, row),
              onRowClick: () => this.view_row(cell, row)
            }, 'View')
          }
        }
      ],
      component_data: Object.values(this.Components),
      component_names: Object.keys(this.Component_Names),
      rows: [],
      pagination: {
        limit: 5
      }
    }
  },
  methods: {
    view_row: function (cell, row) {
      console.log(cell, row)
      const id = row.cells[0].data // get component id from first (hidden) id column
      this.$router.push({
        name: 'ComponentDetail',
        params: { id }
      })
    }
  },
  created: function () {
    if (
      this.Components !== undefined &&
      this.Component_Names !== undefined &&
      this.Components.length === this.Component_Names.length
    ) {
      for (let i = 0; i < this.Component_Names.length; i++) {
        const row = []
        row.push(this.Components[i].component_id)
        row.push(this.Component_Names[i].component_name)
        row.push(this.Components[i].component_type.toLowerCase()
          .split('_')
          .map((s) => s.charAt(0).toUpperCase() + s.substring(1))
          .join(' '))
        this.rows.push(row)
      }
    }
  }
}
</script>
