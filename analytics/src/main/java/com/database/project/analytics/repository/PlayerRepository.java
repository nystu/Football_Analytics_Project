/**
 * PlayerRepository Interface: This interface is responsible for interacting with the database to perform queries related to the 'Player' entity.
 * 
 * Purpose:
 *  • Inherits from JpaRepository, which provides built-in CRUD operations (Create, Read, Update, Delete) for the Player entity.
 *  • Provides a custom method `findAllQuarterbacks()` to fetch only players who play the 'QB' position.
 * 
 * Technologies Involved:
 *  • Spring Data JPA: Provides the mechanism for implementing repository patterns and data access logic automatically.
 *      - JpaRepository is a part of this, and it handles all the low-level SQL logic for you.
 * 
 *  • Hibernate: The ORM (Object-Relational Mapping) tool used by Spring JPA to generate and execute the actual SQL queries.
 *      - Hibernate uses the Player entity class to map Java objects to table rows in the database.
 * 
 *  • @Query Annotation: Used to define custom JPQL (Java Persistence Query Language) queries that go beyond the default JpaRepository methods.
 *      - In this case, the query fetches all players where the 'position' column is 'QB'.
 * 
 * Summary:
 *  • This interface eliminates the need to write boilerplate SQL for basic operations.
 *  • It enables developers to focus on higher-level data interactions by simply declaring method signatures.
 *  • The controller (e.g., PlayerController) calls this repository to execute the database queries.
 * 
 * Date Modified: 2025/04/16
 */

 package com.database.project.analytics.repository;

 import java.util.List;

 import org.springframework.data.jpa.repository.JpaRepository;
 import org.springframework.data.jpa.repository.Query;

 import com.database.project.analytics.model.Player;
 
 public interface PlayerRepository extends JpaRepository<Player, Long> {
 
        /**
         * This method uses the @Query annotation to define a custom JPQL query.
         * It selects all Player objects where the 'position' column is equal to 'QB'.
         * @return List of all Player entities who have the position "QB".
         */
        @Query("SELECT p FROM Player p WHERE p.position = 'QB'")
        List<Player> findAllQuarterbacks();
}