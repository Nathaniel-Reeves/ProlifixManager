<template>
    <Grid :cols="cols" :rows="rows" :pagination="{ 'limit': 5 }" :sort="true"></Grid>
</template>

<script>
import Grid from 'gridjs-vue'

export default {
  name: 'InventoryGrid',
  inventory: {
    Grid
  },
  props: {
    inventory: Object
  },
  data () {
    return {
      cols: ['Item Name', 'Type'],
      inventory_data: Object.values(this.inventory),
      rows: [],
      pagination: {
        limit: 5
      }
    }
  },
  created: function () {
    this.inventory_data.forEach(item => {
      const row = [
        item.item_name,
        item.item_type
      ]
      this.rows.push(row)
    })
  }
}
</script>
