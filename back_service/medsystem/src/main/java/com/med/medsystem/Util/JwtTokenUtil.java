package com.med.medsystem.Util;

import java.security.Key;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.function.Function;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Component;

import com.med.medsystem.config.JwtProperties;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.io.Decoders;
import io.jsonwebtoken.security.Keys;

@Component
public class JwtTokenUtil {
    
    @Autowired
    private JwtProperties jwtProperties;

    private Key getSigningKey(){
        byte[] keyBytes = Decoders.BASE64.decode(jwtProperties.getSecret());
        return Keys.hmacShaKeyFor(keyBytes);
    }

    public String generateToken(UserDetails userDetails){
        Map <String,Object> claims = new HashMap<>();
        return createToken(claims,userDetails.getUsername());
    }

    private String createToken(Map<String,Object> claims,String subject){
        return Jwts.builder()
            .setClaims(claims)
            .setSubject(subject)
            .setIssuedAt(new Date(System.currentTimeMillis()))
            .setExpiration(new Date(System.currentTimeMillis()+jwtProperties.getExpiration()*1000))
            .signWith(getSigningKey(),SignatureAlgorithm.HS256)
            .compact();
    }

    //验证token
    public Boolean validateToken(String token,UserDetails userDetails){
        final String username = extractUsername(token);
        return (username.equals(userDetails.getUsername()) && !isTokenExpired(token));
    }

    //提取用户
    public String extractUsername(String token){
        return extractClaim(token, Claims::getSubject);
    }

    //提取过期时间
    public Date extractExpiration(String token){
        return extractClaim(token,Claims::getExpiration);
    }

    private <T> T extractClaim(String token,Function<Claims,T> claimsResolver){
        final Claims claims = extractAllClaims(token);
        return claimsResolver.apply(claims);
    }

    private Claims extractAllClaims(String token){
        return Jwts.parserBuilder()
            .setSigningKey(getSigningKey())
            .build()
            .parseClaimsJws(token)
            .getBody();
    }
    
    private Boolean isTokenExpired(String token){
        return extractExpiration(token).before(new Date());
    }

}
