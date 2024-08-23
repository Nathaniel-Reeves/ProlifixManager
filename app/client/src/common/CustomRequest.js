export class CustomRequest {
  constructor (sessionKey) {
    // raise error if no session key
    if (!sessionKey) {
      throw new Error('Invalid session key')
    }

    // Data fields
    this.userSessionKey = sessionKey
    this.stale_request = false
    this.payload = {
      upsert: {
        Organizations: [],
        Processes: [],
        Components: [],
        Facilities: [],
        Organization_Names: [],
        People: [],
        Product_Master: [],
        Product_Variant: [],
        Purchase_Orders: [],
        Sales_Orders: [],
        Equipment: [],
        Component_Names: [],
        Users: [],
        Formula_Master: [],
        Item_id: [],
        Manufacturing_Process: [],
        Purchase_Order_Detail: [],
        Sale_Order_Detail: [],
        Sales_Orders_Payments: [],
        Inventory: [],
        Formula_Detail: [],
        Manufacturing_Process_Edges: [],
        Process_Components: [],
        Lot_Numbers: [],
        Inventory_Log: [],
        Ingredient_Brands_Join: [],
        Ingredients_Join: [],
        Component_Brands_Join: [],
        Components_Join: [],
        Inventory_Log_Edges: []
      },
      delete: {
        Organizations: [],
        Processes: [],
        Components: [],
        Facilities: [],
        Organization_Names: [],
        People: [],
        Product_Master: [],
        Product_Variant: [],
        Purchase_Orders: [],
        Sales_Orders: [],
        Equipment: [],
        Component_Names: [],
        Users: [],
        Formula_Master: [],
        Item_id: [],
        Manufacturing_Process: [],
        Purchase_Order_Detail: [],
        Sale_Order_Detail: [],
        Sales_Orders_Payments: [],
        Inventory: [],
        Formula_Detail: [],
        Manufacturing_Process_Edges: [],
        Process_Components: [],
        Lot_Numbers: [],
        Inventory_Log: [],
        Ingredient_Brands_Join: [],
        Ingredients_Join: [],
        Component_Brands_Join: [],
        Components_Join: [],
        Inventory_Log_Edges: []
      }
    }
    this.upsertFileData = {}
    this.deleteFileData = []
    this.customUpsertOrder = []
    this.customDeleteOrder = []
    this.fileIndex = 0
    this.savedFiles = {}
    this.tempKeyLookup = {}

    this.validTables = [
      'Organizations',
      'Processes',
      'Components',
      'Facilities',
      'Organization_Names',
      'People',
      'Product_Master',
      'Product_Variant',
      'Purchase_Orders',
      'Sales_Orders',
      'Equipment',
      'Component_Names',
      'Users',
      'Formula_Master',
      'Item_id',
      'Manufacturing_Process',
      'Purchase_Order_Detail',
      'Sale_Order_Detail',
      'Sales_Orders_Payments',
      'Inventory',
      'Formula_Detail',
      'Manufacturing_Process_Edges',
      'Process_Components',
      'Lot_Numbers',
      'Inventory_Log',
      'Ingredient_Brands_Join',
      'Ingredients_Join',
      'Component_Brands_Join',
      'Components_Join',
      'Inventory_Log_Edges'
    ]
  }

  isStale () {
    return this.stale_request
  }

  setStale () {
    this.stale_request = true
  }

  getSavedFiles () {
    return this.savedFiles
  }

  getTempKeyLookup () {
    return this.tempKeyLookup
  }

  setUpsertOrder (order) {
    if (!(order && Array.isArray(order))) {
      throw new Error('Invalid order, order must be an Array.')
    }

    const tableCount = []

    order.forEach(table => {
      if (tableCount.includes(table)) {
        throw new Error('Invalid table in order, Only one table per order.')
      }
      if (!this.validTables.includes(table)) {
        throw new Error(`Invalid table in order: ${table} not in valid tables.`)
      } else {
        tableCount.push(table)
      }
    })

    this.customUpsertOrder = order
  }

  setDeleteOrder (order) {
    if (!(order && Array.isArray(order))) {
      throw new Error('Invalid order, order must be an Array.')
    }

    const tableCount = []

    order.forEach(table => {
      if (tableCount.includes(table)) {
        throw new Error('Invalid table in order, Only one table per order.')
      }
      if (!this.validTables.includes(table)) {
        throw new Error(`Invalid table in order: ${table} not in valid tables.`)
      } else {
        tableCount.push(table)
      }
    })

    this.customDeleteOrder = order
  }

  upsertRecord (table, record) {
    // validate table, raise error if not table
    if (!this.validTables.includes(table)) {
      console.error('Invalid table')
      return false
    }

    // validate record, raise error if not record
    if (!record) {
      console.error('Invalid record')
      return false
    }

    // Add record to payload
    this.payload.upsert[table].push(record)
    return true
  }

  removeUpsertRecord (table, key, value) {
    const index = this.findIndexInTable(table, key, value, 'upsert')
    if (index === null) {
      return false
    }
    this.payload.upsert[table].splice(index, 1)
    return true
  }

  updateUpsertRecord (table, key, value, record) {
    const index = this.findIndexInTable(table, key, value, 'upsert')
    if (index === null) {
      return this.upsertRecord(table, record)
    }
    this.payload.upsert[table][index] = { ...this.payload.upsert[table][index], ...record }
    return true
  }

  deleteRecord (table, record) {
    // validate table, raise error if not table
    if (!this.validTables.includes(table)) {
      console.error('Invalid table')
      return false
    }

    // validate record, raise error if not record
    if (!record) {
      console.error('Invalid record')
      return false
    }

    // Add record to payload
    this.payload.delete[table].push(record)
    return true
  }

  removeDeleteRecord (table, key, value) {
    const index = this.findIndexInTable(table, key, value, 'delete')
    if (index === null) {
      return false
    }
    this.payload.delete[table].splice(index, 1)
    return true
  }

  updateDeleteRecord (table, key, value, record) {
    const index = this.findIndexInTable(table, key, value, 'delete')
    if (index === null) {
      return this.deleteRecord(table, record)
    }
    this.payload.delete[table][index] = { ...this.payload.delete[table][index], ...record }
    return true
  }

  findIndexInTable (table, key, value, action) {
    // validate table, raise error if not table
    if (!this.validTables.includes(table)) {
      console.error('Invalid table:', table)
      return null
    }

    // validate key, raise error if not key
    if (!key) {
      console.error('Invalid key:', key)
      return null
    }

    // validate value, raise error if not value
    if (!value) {
      console.error('Invalid value:', value)
      return null
    }

    if (!Array.isArray(key)) {
      // Find and return index
      let index = null
      if (action === 'upsert') {
        index = this.payload.upsert[table].findIndex(record => key in record && record[key] === value)
      } else if (action === 'delete') {
        index = this.payload.delete[table].findIndex(record => key in record && record[key] === value)
      } else {
        console.error('Invalid action')
        return null
      }

      if (index >= 0) {
        return index
      } else {
        console.warn('Record not found')
        return null
      }
    } else {
      if (!Array.isArray(value)) {
        console.error('Invalid value:', value)
        return null
      }

      if (key.length !== value.length) {
        console.error('Invalid key and value lengths:', key, value)
        return null
      }

      // Find and return index
      let index = null
      if (action === 'upsert') {
        index = this.payload.upsert[table].findIndex(record => this.compareKeys(record, key, value))
      } else if (action === 'delete') {
        index = this.payload.delete[table].findIndex(record => this.compareKeys(record, key, value))
      } else {
        console.error('Invalid action')
        return null
      }

      if (index >= 0) {
        return index
      } else {
        console.warn('Record not found')
        return null
      }
    }
  }

  compareKeys (record, keys, values) {
    for (let i = 0; i < keys.length; i++) {
      if (!(keys[i] in record) || record[keys[i]] !== values[i]) {
        return false
      }
    }
    return true
  }

  setSessionKey (key) {
    this.userSessionKey = key
  }

  compileRequest () {
    const request = {
      user_session_key: this.userSessionKey,
      payload: this.payload,
      upsert_file_data: this.upsertFileData,
      delete_file_data: this.deleteFileData,
      upsert_order: this.customUpsertOrder,
      delete_order: this.customDeleteOrder
    }
    if (this.customUpsertOrder.length > 0) {
      request.upsert_order = this.customUpsertOrder
    }
    if (this.customDeleteOrder.length > 0) {
      request.delete_order = this.customDeleteOrder
    }
    return request
  }

  printRequest () {
    const req = this.compileRequest()
    console.log('PRINTING REQUEST: ', req)
  }

  async addFile (file, page, idCode, dir, ref_count = 1) {
    // validate file, raise error if not file
    if (!file) {
      console.error('Invalid file')
      return null
    }

    // validate page is a number, raise error if not number
    if (isNaN(page)) {
      console.error('Invalid page number')
      return null
    }

    // validate id_code is a string, raise error if not string
    if (typeof idCode !== 'string') {
      console.error('Invalid id code')
      return null
    }

    // Compact file data to base 64
    const toBase64 = file => new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.readAsDataURL(file)
      reader.onload = () => resolve(reader.result)
      reader.onerror = reject
    })

    // Create file record and save to upsertFileData
    const newFile = {
      filename: file.name,
      filetype: file.type,
      dir: dir,
      page: page,
      size: file.size,
      id_code: idCode,
      data_uri: await toBase64(file),
      ref_count: ref_count
    }
    const customKey = 'file_' + this.fileIndex
    this.upsertFileData[customKey] = newFile
    this.fileIndex += 1
    return customKey
  }

  async deleteFile (hash) {
    // validate hash, raise error if not hash
    if (!hash) {
      console.error('Invalid hash')
      return false
    }

    if (hash.includes('file_')) {
      // Remove hash from upsertFileData
      delete this.upsertFileData[hash]
    } else {
      // Add hash to deleteFileData
      this.deleteFileData.push(hash)
    }
    return true
  }

  async sendRequest (origin) {
    const fetchRequest = origin + '/api/v1/submit'
    // eslint-disable-next-line
    console.log(
      'PUT ' + fetchRequest
    )

    const body = this.compileRequest()
    // eslint-disable-next-line
    this.printRequest()

    const response = await fetch(fetchRequest, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify(body)
    })

    if (response.status === 201) {
      // eslint-disable-next-line
      console.log('Request successful')
    } else {
      // eslint-disable-next-line
      console.log('Request failed')
    }

    try {
      const data = await response.json()
      // eslint-disable-next-line
      console.log('Response Data:', data)
      data.status = response.status
      this.stale_request = data.stale_request
      this.savedFiles = data.data[0].saved_files
      this.tempKeyLookup = data.data[0].temp_key_lookup
      return data
    } catch (error) {
      // eslint-disable-next-line
      console.log('Error parsing response')
      const subData = {
        status: response.status,
        data: [],
        messages: {
          flash: [
            {
              title: 'Response Parsing Error!',
              message: 'Error parsing response from server. ' + error,
              variant: 'danger',
              debug_code: 'RESPONSE_PARSE_ERROR  CustomRequest.js line: 416',
              link: '',
              auto_hide_delay: 5000,
              no_auto_hide: false,
              no_close_button: false,
              visible: true
            }
          ],
          form: {}
        }
      }
      return subData
    }
  }
}

export function genTempKey () {
  return 'temp-' + Math.floor(Math.random() * 100000000)
}

export function isTempKey (key) {
  if (!key) {
    return false
  }
  if (typeof key !== 'string') {
    return false
  }
  return key.includes('temp-')
}
