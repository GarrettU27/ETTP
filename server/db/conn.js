const { MongoClient } = require("mongodb");
const uri = process.env.MONGO_URI;
const client = new MongoClient(uri, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});
 
var _db;
 
module.exports = {
  connectToServer: async function (callback) {
  try {
    const database = client.db('employees');
    _db = database;
    
    if (database) {
        console.log("Successfully connected to MongoDB")
    }
  } finally {
    // Ensures that the client will close when you finish/error
    await client.close();
  }
},
 
  getDb: function () {
    return _db;
  },
};