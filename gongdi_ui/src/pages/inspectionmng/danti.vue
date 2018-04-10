<template>
  <div>
    <div class="">
      <div class="el-input">
        <el-select v-model="companyid" filterable placeholder="请选择公司">
          <el-option
            v-for="company in companies"
            :key="company.id"
            :label="company.company_name"
            :value="company.id">
          </el-option>
        </el-select>
      </div>
      <el-button @click="insert" type="primary" :disabled="!companyid">新增单体</el-button>
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
        prop="comp_name"
        label="所属公司">
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
        fixed="right"
        label="操作"
        width="130">
        <template slot-scope="scope">
          <el-button @click="remove(scope.row)" size="mini" icon="el-icon-delete"></el-button>
          <el-button @click="edit(scope.row)" size="mini" icon="el-icon-edit"></el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-show="Number(total_datas)"
      background
      layout="prev, pager, next"
      :current-page.sync="cur_page"
      @current-change="handleCurrentChange"
      :page-size="page_size"
      :page-count="total_pages">
    </el-pagination>

    <el-dialog
      :title="title"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="handleClose">

      <el-form label-position="right" label-width="100px" :model="insertData" :rules="rules" ref="ruleForm">
        <el-form-item label="单体名称" prop="name">
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
        <el-button @click="resetForm('ruleForm')">取 消</el-button>
        <el-button type="primary" @click="submitForm('ruleForm')">确 定</el-button>
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
        rules: {
          name: [
            { required: true, message: '请输入单体名称', trigger: 'blur' },
          ],
        },
        companyid: '',
        dialogVisible: false,
        page_size: 5,
        cur_page:1,
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
      handleCurrentChange(val) {
        this.$store.dispatch('getDantis', { companyid:this.companyid, page:val, per_page:this.page_size })
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
      resetForm(formName) {
        this.$refs[formName].resetFields();
        this.dialogVisible = false
      },
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.submitData();
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      submitData(){
        var {...insertData} = this.insertData
        if(this.title === '新增单体'){
          insertData['companyid'] = parseInt(this.companyid)
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
          // 删除一条数据之后的页数
          var total_pages =  Math.ceil((this.total_datas-1) / this.page_size)
          this.$store.dispatch('removeDantis',data);
          // 解决删除一条数据后，当前页大于总页数的问题
          var page = this.cur_page > total_pages ? total_pages : this.cur_page;
          this.$store.dispatch('getDantis', { companyid:this.companyid, page:page, per_page:this.page_size })
        })
      },
      handleClose(done) {
        this.$confirm('确认关闭？')
        .then(_ => {
          done();
        })
      }
    },

    computed: {
      total_pages(){
        return Math.ceil(this.total_datas / this.page_size)
      },
      ...mapGetters([
        'dantis',
        'companies',
        'total_datas',
		  ])
    },

    watch:{
      companyid: function(){
        this.$store.dispatch('getDantis', { companyid:this.companyid, page:1, per_page:this.page_size } )
      }
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
