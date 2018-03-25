<template>
  <div>
    <div class="">
      <div class="select">
        <el-select v-model="companyid" filterable placeholder="请选择公司">
          <el-option
            v-for="company in companies"
            :key="company.id"
            :label="company.company_name"
            :value="company.id">
          </el-option>
        </el-select>
        <el-select v-model="dantiid" filterable placeholder="请选择单体">
          <el-option
            v-for="danti in dantis"
            :key="danti.id"
            :label="danti.name"
            :value="danti.id">
          </el-option>
        </el-select>
      </div>
      <el-button @click="insert" type="primary" :disabled="!(companyid && dantiid)">新增部位</el-button>
    </div>

    <el-table
      :data="buweis"
      border
      style="width: 100%">
      <el-table-column
        fixed
        prop="name"
        label="部位名称"
        width="150">
      </el-table-column>
      <el-table-column
        prop="danti_name"
        label="所属单体">
        width="200"
      </el-table-column>
      <el-table-column
        prop="description"
        label="描述">
      </el-table-column>
      <el-table-column
        fixed="right"
        label="操作"
        width="100">
        <template slot-scope="scope">
          <el-button @click="remove(scope.row)" type="text" size="mini" icon="el-icon-delete"></el-button>
          <el-button @click="edit(scope.row)" type="text" size="mini" icon="el-icon-edit"></el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      :title="title"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="handleClose">

      <el-form label-position="right" label-width="100px" :model="insertData">
        <el-form-item label="部位名称">
          <el-input v-model="insertData.name"></el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="insertData.description"></el-input>
        </el-form-item>
      </el-form>

      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitData">确 定</el-button>
      </span>
    </el-dialog>

  </div>
</template>

<script>
  import {mapGetters} from 'vuex'
  export default {
    mounted(){
      this.$store.dispatch('getCompanies')
    },

    data() {
      return {
        companyid: '',
        dantiid: '',
        dialogVisible: false,
        title: '',
        insertData:{
          name: '',
          description: ''
        }
      }
    },

    methods: {
      insert(){
        this.title = '新增部位'
        this.dialogVisible = true
      },
      edit(data){
        this.title = '编辑部位'
        var { ...data_copy } = data
        this.insertData = data_copy
        this.dialogVisible = true
      },
      submitData(){
        var {...insertData} = this.insertData
        if(this.title === '新增部位'){
          insertData['dantiid'] = parseInt(this.dantiid)
          this.$store.dispatch('postBuweis',insertData)
        }
        else if(this.title === '编辑部位'){
          this.$store.dispatch('putBuweis',insertData)
        }
        // 重置form
        this.dialogVisible = false
        this.insertData = {
          name: '',
          description: ''
        }
      },
      remove(data) {
        this.$confirm('此操作將永久刪除該資料, 是否繼續?', '提示', {
          confirmButtonText: '確定',
          cancelButtonText: '取消',
        }).then(() => {
          this.$store.dispatch('removeBuweis',data);
        }).catch(() => {         
        });
      },
      handleClose(done) {
        this.$confirm('确认关闭？')
          .then(_ => {
            done();
          })
          .catch(_ => {});
      }
    },

    computed: {
      ...mapGetters([
        'dantis',
        'companies',
        'buweis'
		  ])
    },

    watch:{
      companyid: function(){
        this.dantiid = ''
        this.$store.commit('setDantis',[])
        this.$store.dispatch('getDantis', this.companyid)
      },
      dantiid: function(){
        this.$store.commit('setBuweis',[])        
        if(Boolean(this.dantiid)){
          this.$store.dispatch('getBuweis', this.dantiid)
        }
      },
    }     
  }
</script>

<style scoped>
  .el-select {
    width: 49%;
  }
  .el-dialog {
    width: 350px !important;
  }
  .select {
    width: 350px;
    margin-right: 20px;
    display: inline-block;
  }
</style>

<style>
  .el-table {
    margin-top: 5px;
  }
</style>
