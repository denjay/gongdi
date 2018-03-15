<template>
  <div>
    <div class="">
      <div class="el-input">
        <el-input
          placeholder="请输入公司id"
          v-model="companyid"
          clearable>
        </el-input>
      </div>
      <el-button @click="getDantis" type="primary" :disabled="!companyid">查询</el-button>
      <el-button @click="insert" type="primary" :disabled="!companyid">新增</el-button>
    </div>

    <el-table
      :data="dantis"
      border
      style="width: 100%">
      <el-table-column
        fixed
        prop="name"
        label="名称"
        width="150">
      </el-table-column>
      <el-table-column
        prop="framework_type"
        label="单体结构类型"
        width="120">
      </el-table-column>
      <el-table-column
        prop="build_type"
        label="单体建筑类型"
        width="120">
      </el-table-column>
      <el-table-column
        prop="dt_area"
        label="单体面积"
        width="100">
      </el-table-column>
      <el-table-column
        prop="dt_plies_num"
        label="单体层数"
        width="120">
      </el-table-column>
      <el-table-column
        prop="eaves_height"
        label="屋檐高度"
        width="120">
      </el-table-column>
      <el-table-column
        prop="build_schedule"
        label="施工进度"
        width="120">
      </el-table-column>
      <el-table-column
        prop="description"
        label="描述"
        width="150">
      </el-table-column>
      <el-table-column
        prop="dantiid"
        label="单体id"
        width="120">
      </el-table-column>
      <el-table-column
        prop="companyid"
        label="公司id"
        width="50">
      </el-table-column>
      <el-table-column
        prop="comp_name"
        label="公司名称">
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
        <el-form-item label="单体名称">
          <el-input v-model="insertData.name"></el-input>
        </el-form-item>
        <el-form-item label="单体结构类型">
          <el-input v-model="insertData.framework_type"></el-input>
        </el-form-item>
        <el-form-item label="单体建筑类型">
          <el-input v-model="insertData.build_type"></el-input>
        </el-form-item>
        <el-form-item label="单体面积">
          <el-input v-model="insertData.dt_area"></el-input>
        </el-form-item>
        <el-form-item label="单体层数">
          <el-input v-model="insertData.dt_plies_num"></el-input>
        </el-form-item>
        <el-form-item label="屋檐高度">
          <el-input v-model="insertData.eaves_height"></el-input>
        </el-form-item>
        <el-form-item label="施工进度">
          <el-input v-model="insertData.build_schedule"></el-input>
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
    data() {
      return {
        companyid: '',
        dialogVisible: false,
        title: '',
        insertData:{
          name: '',
          build_type: '',
          framework_type: '',
          dt_area: '',
          dt_plies_num: '',
          eaves_height: '',
          build_schedule: '',
          description: ''
        }
      }
    },

    methods: {
      getDantis(){
        this.$store.commit('setCompanyid', this.companyid)
        this.$store.dispatch('getDantis')
      },
      insert(){
        this.title = '新增单体'
        this.dialogVisible = true
      },
      edit(data){
        this.title = '编辑单体'
        var { ...data_copy } = data
        this.insertData = data_copy
        this.dialogVisible = true
      },
      submitData(){
        var {...insertData} = this.insertData
        if(this.title === '新增单体'){
          insertData['companyid'] = parseInt(this.companyid)
          console.log(insertData)
          this.$store.dispatch('postDantis',insertData)
        }
        else if(this.title === '编辑单体'){
          this.$store.dispatch('putDantis',insertData)
        }
        // 重置form
        this.dialogVisible = false
        this.insertData = {
          name: '',
          build_type: '',
          framework_type: '',
          dt_area: '',
          dt_plies_num: '',
          eaves_height: '',
          build_schedule: '',
          description: ''
        }
      },
      remove(data) {
        this.$confirm('此操作將永久刪除該資料, 是否繼續?', '提示', {
          confirmButtonText: '確定',
          cancelButtonText: '取消',
        }).then(() => {
          this.$store.dispatch('removeDantis',data);
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
			  'dantis'
		  ])
    }
  }
</script>

<style>
  .el-dialog {
    width: 350px !important;
  }
  .el-input {
    width: 180px;
    margin-right: 20px;
  }
  .el-table {
    margin-top: 5px;
  }
</style>
