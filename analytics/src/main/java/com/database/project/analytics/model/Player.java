/**
 * Player Entity Class: Represents a single row in the 'Player' table of the database.
 * 
 * Purpose:
 *  • Defines all the player attributes such as firstName, lastName, birthDate, position, etc.
 *  • Annotated with @Entity and @Column to map this Java class to a relational database table.
 *  • Enables automatic mapping between Java objects and database rows.
 * 
 * Technologies Involved:
 *  • Spring Boot: A framework that simplifies building full-stack Java applications by handling
 *    common configurations and wiring components together automatically.
 * 
 *  • Hibernate: A powerful ORM (Object-Relational Mapping) tool used by Spring behind the scenes.
 *    It allows Java classes (like this Player class) to be treated as database tables.
 *    Hibernate translates SQL queries to Java and vice versa, reducing the need to write raw SQL.
 * 
 *  • JPA (Java Persistence API): A specification that defines how to manage relational data in Java.
 *    Spring Data JPA provides the interface (like JpaRepository) which makes it easy to
 *    create, read, update, and delete database entries using standard Java methods.
 * 
 * Summary:
 *  • This class acts as the "model" in the MVC architecture.
 *  • It is mapped to the 'Player' table in the MySQL database.
 *  • When data is retrieved through a JPA Repository (like PlayerRepository), Spring and Hibernate
 *    use this class to automatically convert each database row into a Java object.
 * 
 * Date Modified: 2025/4/16
 */


package com.database.project.analytics.model;

import java.time.LocalDate;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "`Player`")
public class Player {

        /**
         * ID specifies the primary key for the Player table.
         * The @GeneratedValue annotation indicates that the value of this field will be AUTO-INCREMENTED
         * The strategy is set to IDENTITY, meaning the database will automatically generate a unique value
         * The Column annotation specifies the name of the column in the database table (Long because it could be a large number)
         */
        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)
        @Column(name = "`PlayerID`")
        private Long playerID;

        /**
         * The @Column annotation specifies the name of the column in the database table
         * The nullable attribute indicates whether this field can be null in the database
         * For FirstName we set nullable = false, meaning it cannot be null
         */
        @Column(name = "`FirstName`", nullable = false)
        private String firstName;

        /**
         * The @Column annotation specifies the name of the column in the database table
         * The nullable attribute indicates whether this field can be null in the database
         * For LastName we set nullable = false, meaning it cannot be null
         */
        @Column(name = "`LastName`", nullable = false)
        private String lastName;

        /**
         * The @Column annotation specifies the name of the column in the database table
         * The nullable attribute indicates whether this field can be null in the database
         * For BirthDate we set nullable = false, meaning it cannot be null
         */
        @Column(name = "`BirthDate`", nullable = false)
        private LocalDate birthDate;

        /**
         * The @Column annotation specifies the name of the column in the database table
         * The nullable attribute indicates whether this field can be null in the database
         * For College we set nullable = false, meaning it cannot be null
         */
        @Column(name = "`College`", nullable = false)
        private String college;

        /**
         * The @Column annotation specifies the name of the column in the database table
         * The nullable attribute indicates whether this field can be null in the database
         * For Weight we set nullable = false, meaning it cannot be null
         */
        @Column(name = "`Weight`", nullable = false)
        private int weight;

        /**
         * The @Column annotation specifies the name of the column in the database table
         * The nullable attribute indicates whether this field can be null in the database
         * For Height we set nullable = false, meaning it cannot be null
         */
        @Column(name = "`Height`", nullable = false)
        private int height;

        /**
         * The @Column annotation specifies the name of the column in the database table
         * The nullable attribute indicates whether this field can be null in the database
         * For Position we set nullable = false, meaning it cannot be null
         */
        @Column(name = "`Position`", nullable = false)
        private String position;


        /**
         * JPA requires a no-argument constructor for entity classes.
         * This constructor is used by Hibernate to create instances of the Player class.
         * Meaning it is used to create a new Player object without any initial values (Yet to be set)
         */
        public Player() {}

        
        /**
         * The CONSTRUCTOR initializes a new Player object with the provided values.
         * It sets the values for firstName, lastName, birthDate, college, weight, height, and position.
         * Constructor is used for creating or updating a Player object with specific values.
         * 
         * @param firstName
         * @param lastName
         * @param birthDate
         * @param college
         * @param weight
         * @param height
         * @param position
         */
        public Player(String firstName, String lastName, LocalDate birthDate, String college, int weight, int height, String position) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.birthDate = birthDate;
        this.college = college;
        this.weight = weight;
        this.height = height;
        this.position = position;
        }


        public Long getPlayerID() {
                return playerID;
        }

        public void setPlayerID(Long playerID) {
                this.playerID = playerID;
        }
        
        // ====================================================

        public String getFirstName() {
                return firstName;
        }

        public void setFirstName(String firstName) {
                this.firstName = firstName;
        }

        // ====================================================

        public String getLastName() {
                return lastName;
        }

        public void setLastName(String lastName) {
                this.lastName = lastName;
        }

        // ====================================================

        public LocalDate getBirthDate() {
                return birthDate;
        }

        public void setBirthDate(LocalDate birthDate) {
                this.birthDate = birthDate;
        }

        // ====================================================

        public String getCollege() {
                return college;
        }

        public void setCollege(String college) {
                this.college = college;
        }

        // ====================================================

        public int getWeight() {
                return weight;
        }

        public void setWeight(int weight) {
                this.weight = weight;
        }

        // ====================================================

        public int getHeight() {
                return height;
        }

        public void setHeight(int height) {
                this.height = height;
        }

        // ====================================================

        public String getPosition() {
                return position;
        }

        public void setPosition(String position) {
                this.position = position;
        }
}