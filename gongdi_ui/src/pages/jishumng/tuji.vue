<template>
  <div>
    <div class="">
      <el-collapse v-model="activeNames">
        <el-collapse-item title="可选筛选项" name="1">
          <div class="select">
            <span>选择部位：</span>
            <el-select v-model="filterData.companyid" filterable clearable placeholder="请选择公司">
              <el-option
                v-for="company in companies"
                :key="company.id"
                :label="company.company_name"
                :value="company.id">
              </el-option>
            </el-select>
            <el-select v-model="filterData.dantiid" filterable clearable placeholder="请选择单体">
              <el-option
                v-for="danti in dantis"
                :key="danti.id"
                :label="danti.name"
                :value="danti.id">
              </el-option>
            </el-select>
            <el-select v-model="filterData.buweiid" filterable clearable placeholder="请选择部位">
              <el-option
                v-for="buwei in buweis"
                :key="buwei.id"
                :label="buwei.name"
                :value="buwei.id">
              </el-option>
            </el-select>
            <br>
            <span>文档名：</span>
            <el-input
              placeholder="请输入文档名"
              v-model="filterData.name"
              clearable>
            </el-input>
          </div>
        </el-collapse-item>
      </el-collapse>
      <el-button @click="getDocs(1)" type="primary">查询</el-button>
      <el-button @click="insert" type="primary">新增文档</el-button>
    </div>

    <el-table
      :data="docs"
      border
      style="width: 100%">
      <el-table-column
        fixed
        prop="code"
        label="编号"
        width="100">
      </el-table-column>
      <el-table-column
        prop="name"
        label="文档名"
        width="150">
      </el-table-column>
      <el-table-column
        prop="buwei_name"
        label="所属部位"
        width="150">
      </el-table-column>
      <el-table-column
        prop="description"
        label="描述">
      </el-table-column>
      <el-table-column
        fixed="right"
        label="下载二维码"
        width="100">
        <template slot-scope="scope">
          <a :href="`/kong/gongdi_mng/v1.0/bw_jishu_qrcode/${scope.row.id}`" :download="scope.row.id">
            <el-button size="mini" icon="el-icon-download"></el-button>
          </a>
        </template>
      </el-table-column>
      <el-table-column
        fixed="right"
        label="操作"
        width="160">
        <template slot-scope="scope">
          <el-button @click="remove(scope.row)" size="mini" icon="el-icon-delete"></el-button>
          <el-button @click="edit(scope.row)" size="mini" icon="el-icon-edit"></el-button>
          <el-button @click="file_manage(scope.row)" size="mini" icon="el-icon-document"></el-button>
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

    <el-dialog class="dialog_file" title="文档附件管理" :visible.sync="dialogVisible_file" :before-close="handleClose">
      <el-table
        :data="doc_files"
        border
        style="width: 100%">
        <el-table-column
          prop="file_name"
          label="文件名">
        </el-table-column>
        <el-table-column
          prop="file_size"
          width="150"
          label="文件大小(kb)">
        </el-table-column>
        <el-table-column
          fixed="right"
          label="操作"
          width="115">
          <template slot-scope="scope">
            <el-button @click="remove_doc_file(scope.row)" size="mini" icon="el-icon-delete"></el-button>
            <a :href="`/kong/gongdi_mng/v1.0/doc_files/${scope.row.id}`">
              <el-button size="mini" icon="el-icon-download"></el-button>
            </a>
          </template>
        </el-table-column>
      </el-table>

      <el-upload
        class="upload-demo"
        ref="upload"
        action="/kong/gongdi_mng/v1.0/doc_files"
        multiple
        name="doc"
        :data={docsid:doc_id}
        :before-remove="beforeRemove"
        :on-success="handleAvatarSuccess"
        :file-list="fileList"
        :auto-upload="false">
        <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
        <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">上传到服务器</el-button>
        <div slot="tip" class="el-upload__tip">可以上传多个文件</div>
      </el-upload>
    </el-dialog>
    
    <el-dialog :title="title" :visible.sync="dialogVisible_doc">
      <el-form label-position="right" label-width="100px" :model="formData" :rules="rules" ref="ruleForm">
        <template v-if="title === '新增文档'">
          <el-form-item label="公司名称" prop="companyid">
            <el-select v-model="formData.companyid" filterable clearable placeholder="请选择公司">
              <el-option
                v-for="company in companies"
                :key="company.id"
                :label="company.company_name"
                :value="company.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="所属单体" prop="dantiid">
            <el-select v-model="formData.dantiid" filterable clearable placeholder="请选择单体">
              <el-option
                v-for="danti in dantis"
                :key="danti.id"
                :label="danti.name"
                :value="danti.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="所属部位" prop="buweiid">
            <el-select v-model="formData.buweiid" filterable clearable placeholder="请选择部位">
              <el-option
                v-for="buwei in buweis"
                :key="buwei.id"
                :label="buwei.name"
                :value="buwei.id">
              </el-option>
            </el-select>
          </el-form-item>
        </template>
        <el-form-item label="编号" prop="code">
          <el-input
            placeholder="请输入文档编号"
            v-model="formData.code"
            clearable>
          </el-input>
        </el-form-item>
        <el-form-item label="文档名称" prop="name">
          <el-input
            placeholder="请输入文档名称"
            v-model="formData.name"
            clearable>
          </el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            type="textarea"
            :rows="2"
            placeholder="请输入内容"
            v-model="formData.description">
          </el-input>
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
  import axios from 'axios'
  import {mapGetters} from 'vuex'
  export default {
    mounted(){
      this.$store.dispatch('tuji/doc/buwei/getCompanies')
    },

    data() {
      return {
        fileList:[],        
        rules: {
          companyid: [
            { required: true, message: '请选择所属公司', trigger: 'change' },
          ],
          dantiid: [
            { required: true, message: '请选择所属单体', trigger: 'change' },
          ],
          buweiid: [
            { required: true, message: '请选择所属部位', trigger: 'change' },
          ],
          code: [
            { required: true, message: '请输入文件编码', trigger: 'blur' },
          ],
          name: [
            { required: true, message: '请输入文档名', trigger: 'blur' },
          ],
          shigong_danwei: [
            { required: true, message: '请输施工单位', trigger: 'blur' },
          ],
        },
        filterData:{
          companyid: '',
          dantiid: '',
          buweiid: null,
          name: null, 
        },
        formData:{
          companyid: '',
          dantiid: '',
          buweiid: null,
          code: null,
          name: null, 
          description: '',
        },
        doc_type:'tuji',
        page_size: 15,
        cur_page:1,
        doc_id: null,
        activeNames: ['1'],
        dialogVisible_doc: false,
        dialogVisible_file: false,
        title: '',
      }
    },

    methods: {
      handleCurrentChange(val) {
        this.getDocs(val)
      },
      getDocs(page){
        this.$store.dispatch('tuji/doc/getDocs', {
          "doc_type":this.doc_type,
          "page":page,
          "per_page":this.page_size,
          "buwei":this.buwei_name,
          "doc_name":this.filterData.name
          })        
      },
      insert(){
        // 新增时先清空表单数据        
        this.title = '新增文档'
        this.dialogVisible_doc = true
        this.formData.name = ''
        this.formData.code = ''
        this.formData.description = ''
      },
      edit(data){
        // 点编辑时，将对应行数据写入表单   
        this.title = '编辑文档'
        this.doc_id = data.id
        this.formData.name = data.name
        this.formData.code = data.code
        this.formData.description = data.description
        this.dialogVisible_doc = true
      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
        this.dialogVisible_doc = false
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
        // 组织表单需要的数据，创建或更新数据        
        var data = {
          doc_type:this.doc_type,
          code:this.formData.code,
          name:this.formData.name,
          buweiid:this.formData.buweiid,
          description:this.formData.description,
        }
        if(this.title === '新增文档'){
          this.$store.dispatch('tuji/doc/postDocs',data)
        }
        else if(this.title === '编辑文档'){
          data["id"] = this.doc_id
          delete data.buweiid          
          this.$store.dispatch('tuji/doc/putDocs',data)
        }
        this.dialogVisible_doc = false
      },
      remove(data) {
        this.$confirm('此操作將永久刪除該資料, 是否繼續?', '提示', {
          confirmButtonText: '確定',
          cancelButtonText: '取消',
        }).then(() => {
          // 删除一条数据之后的页数
          var total_pages =  Math.ceil((this.total_datas-1) / this.page_size)
          // 解决删除一条数据后，当前页大于总页数的问题
          var page = this.cur_page > total_pages ? total_pages : this.cur_page;
          var query_args = {
          "doc_type":this.doc_type,
          "page":page,
          "per_page":this.page_size,
          "buwei":this.buwei_name,
          "doc_name":this.filterData.name
          }
          this.$store.dispatch('tuji/doc/removeDocs',{"doc_type":data.doc_type,"id":data.id,"query_args":query_args});
        })
      },
      file_manage(data){
        this.$store.dispatch('tuji/doc/doc_files/getDocFiles', data.id)  
        this.doc_id = data.id
        this.dialogVisible_file = true      
      },
      handleClose(done) {
        this.fileList = []
        done()
      },
      // upload相关
      submitUpload() {
        this.$refs.upload.submit();
      },
      beforeRemove(file, fileList) {
        return this.$confirm(`确定移除 ${ file.name }？`);
      },
      handleAvatarSuccess(file) {
        this.$store.dispatch('tuji/doc/doc_files/getDocFiles', this.doc_id)
        this.fileList = []
        this.$message({
          message: '文件上传成功',
          type: 'success'
        });
      }, 
      remove_doc_file(data) {
        this.$confirm('此操作將永久刪除該資料, 是否繼續?', '提示', {
          confirmButtonText: '確定',
          cancelButtonText: '取消',
        }).then(() => {
          this.$store.dispatch('tuji/doc/doc_files/removeDocFiles',data);
        })
      },
    },

    computed: {
      total_pages(){
        return Math.ceil(this.total_datas / this.page_size)
      },
      buwei_name(){
        if(Boolean(this.filterData.buweiid)){
          return this.buweis.filter(item => item.id === this.filterData.buweiid)[0]["name"]
        }
      },
      ...mapGetters('tuji/doc/buwei',{
        'dantis':'dantis',
        'companies':'companies',
        'buweis':'buweis',
        }
      ),
      ...mapGetters('tuji/doc/doc_files',{
        'doc_files':'doc_files',
        }
      ),
      ...mapGetters('tuji/doc',{
        'docs':'docs',
        'total_datas':'total_datas',
		  }),
    },

    watch:{
      "filterData.companyid": function(){
        this.filterData.dantiid = ''
        this.$store.commit('tuji/doc/buwei/setDantis',[])
        if(Boolean(this.filterData.companyid)){
          this.$store.dispatch('tuji/doc/buwei/getDantis', {companyid:this.filterData.companyid})
        }
      },
      "filterData.dantiid": function(){
        this.filterData.buweiid = null
        this.$store.commit('tuji/doc/buwei/setBuweis',[])
        if(Boolean(this.filterData.dantiid)){
          this.$store.dispatch('tuji/doc/buwei/getBuweis', this.filterData.dantiid)
        }
      },
      "formData.companyid": function(){
        this.formData.dantiid = ''
        this.$store.commit('tuji/doc/buwei/setDantis',[])
        if(Boolean(this.formData.companyid)){
          this.$store.dispatch('tuji/doc/buwei/getDantis', {companyid:this.formData.companyid})
        }
      },
      "formData.dantiid": function(){
        this.formData.buweiid = null
        this.$store.commit('tuji/doc/buwei/setBuweis',[])
        if(Boolean(this.formData.dantiid)){
          this.$store.dispatch('tuji/doc/buwei/getBuweis', this.formData.dantiid)
        }
      },
    }     
  }
</script>

<style scoped>
  .select span {
    display:inline-block;
    width: 70px;
  }
  .select .el-select {
    margin-bottom: 20px;
  } 
  .el-select {
    width: 200px;
  } 
  .select {
    width: 700px;
    margin-right: 20px;
    display: inline-block;
  }
  .select .el-input {
    margin-bottom: 20px;
  }
  .el-input {
    width: 200px;
  }
  .el-textarea {
    width: 200px;
  }
  .el-button+.el-button {
    margin-left: 0px;
  }
</style>

<style>
  .el-dialog {
    width: 385px;
  }
  .dialog_file .el-dialog {
    width: 700px !important;
  }
  .el-table {
    margin-top: 5px;
  }
  .el-collapse-item__header {
    width: 120px;
    font-size: 16px;
    color: #409eff;
  }
</style>
