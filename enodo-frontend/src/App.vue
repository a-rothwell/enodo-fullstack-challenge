<template>
  <el-container>
    <el-aside width="40%">
      <el-row>
        <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
          <Autocomplete />
        </el-col>
        <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
          <Table />
        </el-col>
      </el-row>
    </el-aside>
    <el-main width=60%>
      <el-row>
        <el-col>
          <el-row>
            <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" style="height: 90vh;">
              <Map />
            </el-col>
          </el-row>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script>
  import Map from './components/Map.vue'
  import Autocomplete from './components/Autocomplete.vue'
  import Table from './components/Table.vue'

  export default {
    name: 'App',
    components: {
      Map,
      Autocomplete,
      Table
    }
  }
</script>