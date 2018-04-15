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
      <el-button @click="insert" type="primary" :disabled="companyid && Boolean(gongdis.length)">新增工地</el-button>
    </div>

    <el-table
      :data="gongdis"
      border
      style="width: 100%">
      <el-table-column
        fixed
        prop="code"
        label="工地代码"
        width="150">
      </el-table-column>
      <el-table-column
        prop="lon"
        label="经度"
        width="80">
      </el-table-column>
      <el-table-column
        prop="lat"
        label="纬度"
        width="80">
      </el-table-column>
      <el-table-column
        prop="starttime"
        label="开工时间"
        width="100">
      </el-table-column>
      <el-table-column
        prop="complete_time"
        label="竣工时间"
        width="120">
      </el-table-column>
      <el-table-column
        prop="build_unit"
        label="建设单位"
        width="120">
      </el-table-column>
      <el-table-column
        prop="design_unit"
        label="设计单位"
        width="120">
      </el-table-column>
      <el-table-column
        prop="monitor_unit"
        label="监理单位"
        width="150">
      </el-table-column>
      <el-table-column
        prop="construct_unit"
        label="土建施工单位"
        width="120">
      </el-table-column>
      <el-table-column
        prop="description"
        label="描述"
        width="150">
      </el-table-column>
      <el-table-column
        fixed="right"
        label="下载二维码"
        width="100">
        <template slot-scope="scope">
          <a :href="`/kong/gongdi_mng/v1.0/gongdis_qrcode/${scope.row.id}`" :download="scope.row.id">
            <el-button size="mini" icon="el-icon-download"></el-button>
          </a>
        </template>
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

    <el-dialog
      :title="title"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="handleClose">

      <el-form label-position="right" label-width="100px" :model="insertData" :rules="rules" ref="ruleForm">
        <el-form-item label="工地代码" prop="code">
          <el-input v-model="insertData.code"></el-input>
        </el-form-item>
        <el-form-item label="经度">
          <el-input v-model.number="insertData.lon"></el-input>
        </el-form-item>
        <el-form-item label="纬度">
          <el-input v-model.number="insertData.lat"></el-input>
        </el-form-item>
        <el-form-item label="开工时间">
          <el-date-picker type="date" placeholder="选择日期" v-model="insertData.starttime" value-format="yyyy-MM-dd" style="width: 100%;"></el-date-picker>
        </el-form-item>
        <el-form-item label="竣工时间">
          <el-date-picker type="date" placeholder="选择日期" v-model="insertData.complete_time" value-format="yyyy-MM-dd" style="width: 100%;"></el-date-picker>          
        </el-form-item>
        <el-form-item label="建设单位">
          <el-input v-model="insertData.build_unit"></el-input>
        </el-form-item>
        <el-form-item label="设计单位">
          <el-input v-model="insertData.design_unit"></el-input>
        </el-form-item>
        <el-form-item label="监理单位">
          <el-input v-model="insertData.monitor_unit"></el-input>
        </el-form-item>
        <el-form-item label="土建施工单位">
          <el-input v-model="insertData.construct_unit"></el-input>
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
          code: [
            { required: true, message: '请输入工地代码', trigger: 'blur' },
          ]
        },
        companyid: '',
        dialogVisible: false,
        title: '',
        insertData:{
          code: '',
          lon: '',
          lat: '',
          starttime: '',
          complete_time: '',
          build_unit: '',
          design_unit: '',
          monitor_unit: '',
          construct_unit: '',
          description: ''
        },
      }
    },

    methods: {
      insert(){
        this.title = '新增工地'
        this.dialogVisible = true
      },
      edit(data){
        this.title = '编辑工地'
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
        if(this.title === '新增工地'){
          insertData['companyid'] = parseInt(this.companyid)
          this.$store.dispatch('postGongdis',insertData)
        }
        else if(this.title === '编辑工地'){
          this.$store.dispatch('putGongdis',insertData)
        }
        // 重置form
        this.dialogVisible = false
        this.insertData = {
          code: '',
          lon: '',
          lat: '',
          starttime: '',
          complete_time: '',
          build_unit: '',
          design_unit: '',
          monitor_unit: '',
          construct_unit: '',
          description: ''
        }
      },
      remove(data) {
        this.$confirm('此操作將永久刪除該資料, 是否繼續?', '提示', {
          confirmButtonText: '確定',
          cancelButtonText: '取消',
        }).then(() => {
          this.$store.dispatch('removeGongdis',data);
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
      ...mapGetters([
        'gongdis',
        'companies'
		  ])
    },

    watch:{
      companyid: function(){
        this.$store.dispatch('getGongdis', this.companyid)
      }
    } 
  }
</script>

<style scoped>
  .el-date-editor {
    width: 180px !important;
  }
  .el-table {
    margin-top: 5px;
  }
  .el-input {
    width: 180px;
    margin-right: 20px;
  }
</style>

<style>
  .el-dialog {
    width: 350px !important;
  }

</style>
