export class CustomRequest {
  constructor (sessionKey) {
    // raise error if no session key
    if (!sessionKey) {
      throw new Error('Invalid session key')
    }

    // Data fields
    this.userSessionKey = sessionKey
    this.payload = {
      upsert: {
        Organizations: [],
        Processes: [],
        Components: [],
        Facilities: [],
        Organization_Names: [],
        People: [],
        Product_Master: [],
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
    this.fileIndex = 0

    this.validTables = [
      'Organizations',
      'Processes',
      'Components',
      'Facilities',
      'Organization_Names',
      'People',
      'Product_Master',
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
    this.payload.upsert[table][index] = record
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
    this.payload.delete[table][index] = record
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
  }

  setSessionKey (key) {
    this.userSessionKey = key
  }

  compileRequest () {
    const request = {
      user_session_key: this.userSessionKey,
      payload: this.payload,
      upsert_file_data: this.upsertFileData,
      delete_file_data: this.deleteFileData
    }
    return request
  }

  printRequest () {
    const req = this.compileRequest()
    console.log('PRINTING REQUEST: ', req)
  }

  async addFile (file, page, idCode, dir) {
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
      data_uri: await toBase64(file)
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
    console.log(body)

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
      console.log(response)
    }

    try {
      const data = await response.json()
      data.status = response.status
      // eslint-disable-next-line
      console.log(data)
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
              debug_code: 'RESPONSE_PARSE_ERROR  CustomRequest.js line: 346',
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