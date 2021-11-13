<template>
    <el-table
      :data="tableData"
      style="width: 100%">
      <el-table-column
        prop="property"
        label="Full Address">
      </el-table-column>
      <el-table-column prop="class_desc" label="Class Description">
      </el-table-column>
      <el-table-column>
        <template slot-scope="scope">
            <el-button
            @click.native.prevent="deleteRow(scope.$index, tableData)"
            type="danger"
            icon="el-icon-delete"
            circle>
            </el-button>
      </template>
      </el-table-column>
    </el-table>
</template>

<script>
import axios from 'axios'
export default {
    methods: {
      deleteRow(index, rows) {
        console.log(rows[index])
        this.$root.$emit('remove_marker', rows[index]);
        axios.post("http://localhost:8000/selected",{"property":rows[index]["property"], "selected":0})
        rows.splice(index, 1);
        
      }
    },
  name: 'Table',
  data() {
        return {
          tableData: []
        }
      },
    mounted() {
        this.$root.$on('add_table_data', data => {
            this.tableData.push(data)
        });
        axios.post("http://localhost:8000/search",{ "selected":1}).then((response) => {
            console.log(response.data)
            this.tableData = response.data["properties"]
            for (const item of response.data["properties"]) {
                this.$root.$emit('add_marker', {"lat-long":[item["lat"], item["long"]], "property":item["property"]});
            }
        })
    }

}
</script>