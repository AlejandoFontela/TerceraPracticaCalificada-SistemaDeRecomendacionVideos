using System;
using System.Threading;
using StackExchange.Redis;
using MongoDB.Driver;
using MongoDB.Bson;

namespace Worker
{
    public class Program
    {
        private static IMongoClient? _mongoClient;
        private static IMongoDatabase? _mongoDatabase;

        public static int Main(string[] args)
        {
            try
            {
                bool conexionMongo = false;

                while (true)
                {
                    Thread.Sleep(10000);

                    if (!conexionMongo)
                    {
                        conexionMongo = ConexionMongo();
                    }
                }
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine(ex.ToString());
                return 1;
            }
        }

        private static bool ConexionMongo()
        {
            try
            {
                var connectionString = "mongodb://mongo-contenedor:27017/tiktok_db";
                var mongoClient = new MongoClient(connectionString);
                var mongoDatabase = mongoClient.GetDatabase("tiktok_db");
                Console.WriteLine("Conexion exitosa con MongoDb");

                var videosCollection = mongoDatabase.GetCollection<BsonDocument>("videos");

                var redis = ConnectionMultiplexer.Connect("redis-contenedor");
                var db = redis.GetDatabase();
                var keys = redis.GetServer("redis-contenedor", 6379).Keys();

                foreach (var key in keys)
                {
                    var videoId = key.ToString();
                    var watchTime = db.HashGet(videoId, "watch_time").ToString();
                    var genre = db.HashGet(videoId, "genre").ToString();

                    var document = new BsonDocument
                    {
                        { "_id", videoId },
                        { "watch_time", watchTime },
                        { "genre", genre }
                    };

                    videosCollection.InsertOne(document);
                }

                Console.WriteLine("Datos de Redis insertados en MongoDB correctamente.");

                return true;
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine($"Error de conexion con MongoDb: {ex.Message}");
                return false;
            }
        }

    }
}
