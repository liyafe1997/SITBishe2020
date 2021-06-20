<template>
  <div>
    <div>
      <md-dialog :md-active.sync="modifydialog.show">
        <md-dialog-title>修改商品(ID={{modifydialog.itemdata.id}})</md-dialog-title>

        <div style="padding:20px;">
          <md-field>
            <label>名称</label>
            <md-input v-model="modifydialog.itemdata.name"></md-input>
          </md-field>
          <md-field>
            <label>数量</label>
            <md-input v-model="modifydialog.itemdata.number" type="number"></md-input>
          </md-field>
          <md-field>
            <label>仓库</label>
            <md-input v-model="modifydialog.itemdata.place"></md-input>
          </md-field>
        </div>
        <md-dialog-actions>
          <md-button class="md-primary" @click="modifydialog.show = false">取消</md-button>
          <md-button class="md-primary" @click="confirmModifyItem">确定</md-button>
        </md-dialog-actions>
      </md-dialog>
    </div>
    <md-dialog-alert :md-active.sync="popupdialog" :md-content="dialogcontent" md-confirm-text="好" />

    <md-dialog-confirm
      :md-active.sync="confirmdialog"
      md-title="删除商品"
      md-content="确定要删除该商品吗?"
      md-confirm-text="确定"
      md-cancel-text="取消"
      @md-confirm="confirmDeleteItem"
    />
    <md-table
      v-model="store_items"
      :table-header-color="tableHeaderColor"
    >
      <md-table-row slot="md-table-row" slot-scope="{ item }">
        <md-table-cell md-label="ID">{{ item.id }}</md-table-cell>
        <md-table-cell md-label="商品名">{{ item.name }}</md-table-cell>
        <md-table-cell md-label="数量">{{ item.number }}</md-table-cell>
        <md-table-cell md-label="仓库">{{ item.place }}</md-table-cell>
        <md-table-cell md-label="操作"  v-if="role==4 ? false : true">
          <md-button v-bind:itemid="item.id" v-on:click="deleteitem($event)">删除</md-button>
          <md-button
            class="md-primary"
            v-bind:itemid="item.id"
            v-bind:itemname="item.name"
            v-bind:itemnumber="item.number"
            v-bind:itemplace="item.place"
            v-on:click="modifyitem($event)"
          >修改</md-button>
        </md-table-cell>
      </md-table-row>
    </md-table>
  </div>
</template>

<script>
import Cookies from "js-cookie";
import Vue from "vue";
import VueResource from "vue-resource";
Vue.use(VueResource);
export default {
  name: "store-table",
  props: {
    tableHeaderColor: {
      type: String,
      default: ""
    }
  },
  data: function() {
    return {
      dialogcontent: "",
      popupdialog: false,
      deleteitemid: 0,
      confirmdialog: false,

      modifydialog: {
        show: false,
        itemdata: {}
      },

      selected: [],
      currentusername: "",
      store_items: [],
      role: -1
    };
  },
  mounted() {
    /*
    Vue.http.get("/checklogin").then(
      function(res) {
        if (res.status != 200) {
          window.location.href = "/index.html";
        }
      },
      function() {
        //document.write("Back-End");
      }
    ),*/
    this.role = Cookies.get("role");
    this.getData();
  },
  methods: {
    getData() {
      Vue.http.get("/get_all_store_item").then(response => {
        this.store_items = response.body;
      });
    },
    deleteitem: function(e) {
      var itemid = e.currentTarget.getAttribute("itemid");
      this.deleteitemid = itemid;
      this.confirmdialog = true;
    },
    modifyitem: function(e) {
      this.modifydialog.itemdata.id = e.currentTarget.getAttribute("itemid");
      this.modifydialog.itemdata.name = e.currentTarget.getAttribute(
        "itemname"
      );
      this.modifydialog.itemdata.number = e.currentTarget.getAttribute(
        "itemnumber"
      );
      this.modifydialog.itemdata.place = e.currentTarget.getAttribute(
        "itemplace"
      );
      this.modifydialog.show = true;
      window.console.log(this.modifydialog.itemdata);
    },
    confirmModifyItem() {
      Vue.http
        .get("/update_store_item_by_id", {
          params: {
            id: this.modifydialog.itemdata.id,
            name: this.modifydialog.itemdata.name,
            number: this.modifydialog.itemdata.number,
            place: this.modifydialog.itemdata.place
          }
        })
        .then(response => {
          window.console.log(response.body);
          this.users_items = response.body;
          if (response.body == "ok") {
            this.modifydialog.show = false;
            this.dialogcontent = "修改成功";
            this.popupdialog = true;
            this.getData();
          } else {
            this.modifydialog.show = false;
            this.dialogcontent = "修改失败";
            this.popupdialog = true;
          }
        });
      this.modifydialog.show = false;
    },

    confirmDeleteItem() {
      Vue.http
        .get("/delete_store_item_by_id", { params: { id: this.deleteitemid } })
        .then(response => {
          window.console.log(response.body);
          this.users_items = response.body;
          if (response.body == "ok") {
            this.dialogcontent = "删除成功";
            this.popupdialog = true;
            this.getData();
          } else {
            this.dialogcontent = "删除失败";
            this.popupdialog = true;
          }
        });
    }
  },
  watch: {
    modifydialog: {
      handler(newName, oldName) {
        if (newName == false) {
          this.dialogDismiss();
        }
      }
    }
  }
};
</script>
