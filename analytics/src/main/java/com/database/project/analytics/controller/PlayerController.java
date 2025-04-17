/**
 * PlayerController Class:
 * Acts as the controller layer in the Spring Boot application that handles incoming HTTP requests 
 * related to Player data. This class maps URLs to backend operations and sends responses (usually JSON) 
 * back to the client.
 * 
 * Purpose:
 *  • Defines RESTful API endpoints for interacting with Player data.
 *  • Uses the PlayerRepository interface to perform data operations without directly accessing the database.
 *  • Returns data in JSON format by default (thanks to @RestController), making it easily consumable by frontends like React or plain JavaScript.
 * 
 * Technologies Involved:
 *  • Spring Web (Spring MVC): Provides annotations like @RestController, @RequestMapping, @GetMapping, etc., to expose HTTP endpoints.
 *  • Dependency Injection (DI): The PlayerRepository is injected into this controller through constructor injection, allowing the controller to access database methods indirectly.
 *  • Spring Boot Starter Web: Automatically sets up embedded Tomcat, JSON serialization, request mapping, and other web features.
 * 
 * Examples Of HTTP Endpoint Mappings:
 *  • GET /api/players
 *      - Retrieves all players from the database.
 *      - Calls playerRepository.findAll().
 * 
 *  • GET /api/players/{id}
 *      - Retrieves a single player by their PlayerID.
 *      - Uses @PathVariable to extract 'id' from the URL.
 *      - Calls playerRepository.findById(id).
 * 
 *  • GET /api/players/qbs
 *      - Retrieves all players whose position is "QB".
 *      - Calls custom repository method playerRepository.findAllQuarterbacks().
 * 
 * Summary:
 *  • This class serves as the "Controller" in the MVC (Model-View-Controller) architecture.
 *  • It acts as the bridge between frontend HTTP requests and backend data operations.
 *  • All data returned from this controller is serialized into JSON format automatically.
 * 
 * Date Modified: 2025/04/16
 */

 package com.database.project.analytics.controller;

 import java.util.List;
 
 import org.springframework.web.bind.annotation.GetMapping;
 import org.springframework.web.bind.annotation.PathVariable;
 import org.springframework.web.bind.annotation.RequestMapping;
 import org.springframework.web.bind.annotation.RestController;
 
 import com.database.project.analytics.model.Player;
 import com.database.project.analytics.repository.PlayerRepository;
 
 @RestController
 @RequestMapping("/api/players")
 public class PlayerController {
 
        // Injecting the PlayerRepository using constructor-based dependency injection.
        private final PlayerRepository playerRepository;

        public PlayerController(PlayerRepository playerRepository) {
                this.playerRepository = playerRepository;
        }
 
        /**
         * Endpoint: GET /api/players
         * Description: Retrieves and returns a list of all players in the database.
         * @return List<Player> - all player records
         */
        @GetMapping
        public List<Player> getAllPlayers() {
                return playerRepository.findAll();
        }
 
        /**
         * Endpoint: GET /api/players/{id}
         * Description: Retrieves and returns a single player by their unique PlayerID.
         * If no player is found with the given ID, returns null
         * @param id - ID of the player to retrieve
         * @return Player object with matching ID or null
         */
        @GetMapping("/{id}")
        public Player getPlayerById(@PathVariable Long id) {
                return playerRepository.findById(id).orElse(null);
        }
 
        /**
         * Endpoint: GET /api/players/qbs
         * Description: Retrieves and returns all players whose position is listed as "QB".
         * Uses a custom method in PlayerRepository to filter results.
         * 
         * @return List<Player> - all quarterbacks in the database
         */
        @GetMapping("/qbs")
        public List<Player> getAllQBs() {
                return playerRepository.findAllQuarterbacks();
        }
}