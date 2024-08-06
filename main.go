package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"path/filepath"
)

type Card struct {
	Title       string `json:"title"`
	Description string `json:"description"`
	AudioURL    string `json:"audioUrl"`
	ImageURL    string `json:"imageUrl"`
}

type CardDetails struct {
	Cards []Card `json:"cards"`
}

func main() {
	http.HandleFunc("/", serveHTML)
	http.HandleFunc("/submit", corsMiddleware(submitHandler))

	fmt.Println("Server started at http://localhost:8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

func serveHTML(w http.ResponseWriter, r *http.Request) {
	p := filepath.Join("static", "index.html")
	http.ServeFile(w, r, p)
}

func submitHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Invalid request method", http.StatusMethodNotAllowed)
		return
	}

	var cardDetails CardDetails
	if err := json.NewDecoder(r.Body).Decode(&cardDetails); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	// Process the card details (e.g., save to a database)
	// For now, just print to the console
	fmt.Printf("Received card details: %+v\n", cardDetails)
	fmt.Println("################### successfully got data ######################")
	fmt.Println("")

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{"status": "success"})
}

func corsMiddleware(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusNoContent)
			return
		}

		next(w, r)
	}
}
