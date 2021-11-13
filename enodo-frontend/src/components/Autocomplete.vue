<template>
    <el-row>
        <el-col>
            <h1>Search</h1>
            <el-autocomplete class="inline-input" v-model="selection" :fetch-suggestions="querySearch" style="width: 100%;"
                placeholder="Search for a property" :trigger-on-focus="false" @select="handleSelect"></el-autocomplete>
        </el-col>
    </el-row>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Table',
  data() {
    return {
      links: [],
      selection: ''
      };
    },
    methods: {
      querySearch(queryString, cb) {
        console.log(queryString)
        axios.post("http://localhost:8000/search",{"query_string":queryString, "limit":10, "selected":0}).then((response) => {
            var data = response.data["properties"]
            cb(data)
        })
      },
      handleSelect(item) {
        axios.post("http://localhost:8000/selected",{"property":item["property"], "selected":1})
        this.$root.$emit('add_table_data', item);
        this.$root.$emit('add_marker', {"lat-long":[item["lat"], item["long"]], "property":item["property"]});
        this.selection = ''
      }
    }
  }
</script>